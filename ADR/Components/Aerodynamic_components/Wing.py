from ADR.Components.Aerodynamic_components.Aerodynamic_surface import (
    Aerodynamic_surface,
)


class Wing(Aerodynamic_surface):
    def __init__(self, data):
        super().__init__(data)

        self.calc_area()

    def calc_area(self):
        self.area = 2 * (self.section1.area + self.section2.area)
