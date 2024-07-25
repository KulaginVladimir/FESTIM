from festim import VolumeQuantity
import fenics as f
import numpy as np


class AverageVolume(VolumeQuantity):
    """
    Computes the average value of a field in a given volume
    int(f dx) / int (1 * dx)

    Args:
        field (str, int):  the field ("solute", 0, 1, "T", "retention")
        volume (int): the volume id

    Attributes:
        field (str, int):  the field ("solute", 0, 1, "T", "retention")
        volume (int): the volume id
        title (str): the title of the derived quantity
        show_units (bool): show the units in the title in the derived quantities
            file
        function (dolfin.function.function.Function): the solution function of
            the field

    Notes:
        Units are in H/m3 for hydrogen concentration and K for temperature
    """

    def __init__(self, field, volume: int) -> None:
        super().__init__(field=field, volume=volume)

    @property
    def title(self):
        quantity_title = f"Average {self.field} volume {self.volume}"
        if self.show_units:
            if self.field == "T":
                return quantity_title + " (K)"
            else:
                return quantity_title + " (H m-3)"
        else:
            return quantity_title

    def compute(self):
        return f.assemble(self.function * self.dx(self.volume)) / f.assemble(
            1 * self.dx(self.volume)
        )


class AverageVolumeCylindrical(AverageVolume):
    """
    Computes the average value of a field in a given volume
    int(f dx) / int (1 * dx)
    dx is the volume measure in cylindrical coordinates.
    dx = r dr dz dtheta

    Note: for particle fluxes J is given in H/s, for heat fluxes J is given in W

    Args:
        field (str, int):  the field ("solute", 0, 1, "T", "retention")
        volume (int): the volume id
        title (str): the title of the derived quantity
        show_units (bool): show the units in the title in the derived quantities
            file
        function (dolfin.function.function.Function): the solution function of
            the field
        azimuth_range (tuple, optional): Range of the azimuthal angle
            (theta) needs to be between 0 and 2 pi. Defaults to (0, 2 * np.pi).
    """

    def __init__(self, field, volume, z, azimuth_range=(0, 2 * np.pi)) -> None:
        super().__init__(field=field, volume=volume)
        self.r = None
        self.z = z
        self.azimuth_range = azimuth_range

    @property
    def azimuth_range(self):
        return self._azimuth_range

    @azimuth_range.setter
    def azimuth_range(self, value):
        if value[0] < 0 or value[1] > 2 * np.pi:
            raise ValueError("Azimuthal range must be between 0 and pi")
        self._azimuth_range = value

    def compute(self):

        if self.r is None:
            mesh = (
                self.function.function_space().mesh()
            )  # get the mesh from the function
            rthetaz = f.SpatialCoordinate(mesh)  # get the coordinates from the mesh
            self.r = rthetaz[0]  # only care about r here

        values = f.assemble(self.function * self.r * self.z * self.dx(self.volume)) * (
            self.azimuth_range[1] - self.azimuth_range[0]
        )

        # volume = f.assemble(1 * self.r * self.z * self.dx(self.volume)) * (
        #     self.azimuth_range[1] - self.azimuth_range[0]
        # )
        volume = f.assemble(1 * self.r * self.z * self.dx(self.volume)) * (
            self.azimuth_range[1] - self.azimuth_range[0]
        )

        avg_vol = values / volume
        avg_vol *= self.azimuth_range[1] - self.azimuth_range[0]

        return avg_vol


class AverageVolumeSpherical(AverageVolume):
    """
    Computes the average value of a field in a given volume
    int(f dx) / int (1 * dx)
    dx is the volume measure in cylindrical coordinates.
    dx = rho dtheta dphi

    Note: for particle fluxes J is given in H/s, for heat fluxes J is given in W

    Args:
        field (str, int):  the field ("solute", 0, 1, "T", "retention")
        volume (int): the volume id
        title (str): the title of the derived quantity
        show_units (bool): show the units in the title in the derived quantities
            file
        function (dolfin.function.function.Function): the solution function of
            the field
        azimuth_range (tuple, optional): Range of the azimuthal angle
            (theta) needs to be between 0 and pi. Defaults to (0, np.pi)
        polar_range (tuple, optional): Range of the polar angle
            (phi) needs to be between - pi and pi. Defaults to (-np.pi, np.pi)
    """

    def __init__(
        self, field, volume, azimuth_range=(0, np.pi), polar_range=(-np.pi, np.pi)
    ) -> None:
        super().__init__(field=field, volume=volume)
        self.r = None
        self.azimuth_range = azimuth_range
        self.polar_range = polar_range

    @property
    def polar_range(self):
        return self._polar_range

    @polar_range.setter
    def polar_range(self, value):
        if value[0] < -np.pi or value[1] > np.pi:
            raise ValueError("Polar range must be between - pi and pi")
        self._polar_range = value

    @property
    def azimuth_range(self):
        return self._azimuth_range

    @azimuth_range.setter
    def azimuth_range(self, value):
        if value[0] < 0 or value[1] > np.pi:
            raise ValueError("Azimuthal range must be between 0 and pi")
        self._azimuth_range = value

    def compute(self):

        if self.r is None:
            mesh = (
                self.function.function_space().mesh()
            )  # get the mesh from the function
            rthetaphi = f.SpatialCoordinate(mesh)  # get the coordinates from the mesh
            self.r = rthetaphi[0]  # only care about r here

        values = (
            f.assemble(self.function * self.r**2 * self.dx(self.volume))
            * (self.polar_range[1] - self.polar_range[0])
            * (-np.cos(self.azimuth_range[1]) + np.cos(self.azimuth_range[0]))
        )

        volume = (
            f.assemble(1 * self.r**2 * self.dx(self.volume))
            * (self.polar_range[1] - self.polar_range[0])
            * (-np.cos(self.azimuth_range[1]) + np.cos(self.azimuth_range[0]))
        )

        avg_vol = values / volume

        return avg_vol
