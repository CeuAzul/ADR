from ADR.Components.Aerodynamic_components.Aerodynamic_surface import (
    Aerodynamic_surface,
)


class VS(Aerodynamic_surface):
    def __init__(self, data):
        super().__init__(data)

        self.utilidade_do_EV = "Nenhuma irmao, sai dessa vida!"

        self.calc_area()

    def calc_area(self):
        self.area = self.section1.area + self.section2.area
