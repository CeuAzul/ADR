from ADR.Components.Aerodynamic_components.Airfoil import Airfoil

class Aerodynamic_section():
    def __init__(self, data):

        self.airfoil_name = data.get("airfoil_name")
        self.span = data.get("span")
        self.chord1 = data.get("chord1")
        self.chord2 = data.get("chord2")
        self.twist1 = data.get("twist1")
        self.twist2 = data.get("twist2")

        self.airfoil = Airfoil(data={'airfoil_name': self.airfoil_name})
        self.area = self.calc_area()
        self.MAC = self.calc_MAC()

    def calc_area(self):
        # TODO: Jonny is going to put his area code here
        return (self.chord1 + self.chord2) * self.span

    def calc_MAC(self):
        return self.chord1 - (2 * (self.chord1 - self.chord2) *
                              (0.5 * self.chord1 + self.chord2) /
                              (3 * (self.chord1 + self.chord2)))
