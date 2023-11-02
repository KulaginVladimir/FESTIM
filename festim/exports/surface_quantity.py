import festim as F
import csv


class SurfaceQuantity:
    """Export SurfaceQuantity

    Args:
        field (festim.Species): species for which the surface flux is computed
        surface_subdomain (festim.SurfaceSubdomain1D): surface subdomain
        filename (str, optional): name of the file to which the surface flux is exported

    Attributes:
        field (festim.Species): species for which the surface flux is computed
        surface_subdomain (festim.SurfaceSubdomain1D): surface subdomain
        filename (str): name of the file to which the surface flux is exported
        write_to_file (bool): True if the data is exported to a file
    """

    def __init__(self, field, surface_subdomain, filename: str = None) -> None:
        self.field = field
        self.surface_subdomain = surface_subdomain
        self.filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value is None:
            self._filename = None
        elif not isinstance(value, str):
            raise TypeError("filename must be of type str")
        elif not value.endswith(".csv"):
            raise ValueError("filename must end with .csv")
        self._filename = value

    @property
    def surface_subdomain(self):
        return self._surface_subdomain

    @surface_subdomain.setter
    def surface_subdomain(self, value):
        if not isinstance(value, (int, F.SurfaceSubdomain1D)) or isinstance(
            value, bool
        ):
            raise TypeError("surface should be an int or F.SurfaceSubdomain1D")
        self._surface_subdomain = value

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        # check that field is festim.Species
        if not isinstance(value, (F.Species, str)):
            raise TypeError("field must be of type festim.Species")

        self._field = value

    @property
    def write_to_file(self):
        if self.filename is None:
            return False
        else:
            return True

    def write(self, t):
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([t, self.value])
