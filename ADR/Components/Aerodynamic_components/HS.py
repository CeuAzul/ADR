from ADR.Components.Aerodynamic_components.Aerodynamic_surface import (
    Aerodynamic_surface,
)
import numpy as np


class HS(Aerodynamic_surface):
    def __init__(self, data):
        super().__init__(data)

        self.calc_area()

    def calc_area(self):
        self.area = 2 * (self.section1.area + self.section2.area)

    def update_alpha(self, alpha_airplane):
        self.attack_angle = self.incidence - alpha_airplane

    def set_incidence_range(self, alpha_plane_min, alpha_plane_max):
        self.incidence_range = np.arange(
            alpha_plane_min + self.stall_min, alpha_plane_max + self.stall_max + 1
        )
