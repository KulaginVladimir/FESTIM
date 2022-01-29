from FESTIM import DerivedQuantity
import fenics as f


class TotalVolume(DerivedQuantity):
    def __init__(self, field, volume) -> None:
        super().__init__(field)
        self.volume = volume
        self.title = "Total {} volume {}".format(self.field, self.volume)

    def compute(self):
        return f.assemble(self.function*self.dx(self.volume))


class TotalSurface(DerivedQuantity):
    def __init__(self, field, surface) -> None:
        super().__init__(field)
        self.surface = surface
        self.title = "Total {} surface {}".format(self.field, self.surface)

    def compute(self):
        return f.assemble(self.function*self.ds(self.surface))
