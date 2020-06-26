import pandas as pd
import numpy as np


from ADR.Core.import_functions import (
    import_airfoil_aerodynamic_data,
    import_airfoil_coordinates,
)


class Airfoil:
    def __init__(self, data):
        self.name = data.get("airfoil_name")

        self.Cl_alpha, self.Cd_alpha, self.Cm_alpha = import_airfoil_aerodynamic_data(
            self.name
        )
        self.airfoil_x_coords, self.airfoil_y_coords = import_airfoil_coordinates(
            self.name
        )

        self.import_camber_line()

        self.generate_upper_surface_coordinates()
        self.generate_inner_surface_coordinates()
        self.calc_perimeter()
        self.calc_area()

    def __str__(self):
        return self.name

    def get_Cl(self, alpha):
        Cl = np.interp(alpha, self.Cl_alpha.index.values, self.Cl_alpha["Cl"])
        return Cl

    def get_Cd(self, alpha):
        Cd = np.interp(alpha, self.Cd_alpha.index.values, self.Cd_alpha["Cd"])
        return Cd

    def get_Cm(self, alpha):
        Cm = np.interp(alpha, self.Cm_alpha.index.values, self.Cm_alpha["Cm"])
        return Cm

    def generate_upper_surface_coordinates(self):

        self.n = self.airfoil_x_coords.size
        # número de elementos do vetor de coordenadas horizontais

        self.minpos = np.argmin(self.airfoil_x_coords)
        # posição do menor valor no vetor de coordenadas horizontais,
        # determina a posição do bordo de ataque

        self.airfoil_x_coords_ext = np.flip(
            self.airfoil_x_coords[0: self.minpos])
        # coordenadas horizontais do extradorso

        self.airfoil_y_coords_ext = np.flip(
            self.airfoil_y_coords[0: self.minpos])
        # coordenadas verticais do extradorso

        self.n_ext = self.airfoil_x_coords_ext.size
        # número de elementos do vetor de coordenadas horizontais do extradorso

    def generate_inner_surface_coordinates(self):

        self.airfoil_x_coords_int = self.airfoil_x_coords[
            self.minpos: self.n - 1
        ]
        # coordenadas horizontais do intradorso

        self.airfoil_y_coords_int = self.airfoil_y_coords[
            self.minpos: self.n - 1
        ]
        # coordenadas verticais do intradorso

        self.n_int = (self.airfoil_x_coords_int.size)
        # número de elementos do vetor de coordenadas horizontais do intradorso

    def calc_perimeter(self):

        self.delta_perimeter_array_ext = np.empty([self.n_ext - 1])
        # vetor contando as parcelas de perimetro do extradorso

        self.delta_perimeter_array_int = np.empty([self.n_int - 1])
        # vetor contando as parcelas de perimetro do intradorso

        for i in range(0, self.n_ext - 2):
            delta_perimeter_i_ext = (
                (self.airfoil_x_coords_ext[i + 1]
                 - self.airfoil_x_coords_ext[i]) ** 2
                + (self.airfoil_y_coords_ext[i + 1]
                    - self.airfoil_y_coords_ext[i]) ** 2
            ) ** 0.5
            self.delta_perimeter_array_ext[i] = delta_perimeter_i_ext
        perimeter_ext = np.sum(self.delta_perimeter_array_ext)
        # perímetro do extradorso do perfil

        for i in range(0, self.n_int - 2):
            delta_perimeter_i_int = (
                (self.airfoil_x_coords_int[i + 1]
                 - self.airfoil_x_coords_int[i]) ** 2
                + (self.airfoil_y_coords_int[i + 1]
                    - self.airfoil_y_coords_int[i]) ** 2
            ) ** 0.5
            self.delta_perimeter_array_int[i] = delta_perimeter_i_int
        perimeter_int = np.sum(self.delta_perimeter_array_int)
        # perímetro do intradorso do perfil

        self.perimeter = perimeter_ext + perimeter_int
        # perimetro total do perfil

        self.sum_perimeter_ext_pos = np.empty([self.n_ext - 1])
        sum_perimeter_ext_pos_i = 0
        for i in range(0, self.n_ext - 2):
            sum_perimeter_ext_pos_i = (
                sum_perimeter_ext_pos_i + self.delta_perimeter_array_ext[i]
            )
            self.sum_perimeter_ext_pos[i] = sum_perimeter_ext_pos_i

        self.sum_perimeter_int_pos = np.empty([self.n_int - 1])
        sum_perimeter_int_pos_i = 0
        for i in range(0, self.n_int - 2):
            sum_perimeter_int_pos_i = (
                sum_perimeter_int_pos_i + self.delta_perimeter_array_int[i]
            )
            self.sum_perimeter_int_pos[i] = sum_perimeter_int_pos_i

    def calc_area(self):

        self.delta_area_array_ext = np.empty([self.n_ext - 1])
        # vetor contando as parcelas de área
        # determinadas pelo extradordo e a linha de corda

        self.delta_area_array_int = np.empty([self.n_int - 1])
        # vetor contando as parcelas de área
        # determinadas pelo intradordo e a linha de corda

        for i in range(0, self.n_ext - 2):
            delta_area_ext_i = (
                (self.airfoil_y_coords_ext[i]
                 + self.airfoil_y_coords_ext[i + 1])
                * (self.airfoil_x_coords_ext[i + 1] - self.airfoil_x_coords_ext[i])
                * 0.5
            )
            self.delta_area_array_ext[i] = delta_area_ext_i
        area_ext = np.sum(self.delta_area_array_ext)
        # área determinada pelo extradordo e a linha de corda
        for i in range(0, self.n_int - 2):
            delta_area_int_i = (
                (self.airfoil_y_coords_int[i]
                 + self.airfoil_y_coords_int[i + 1])
                * (self.airfoil_x_coords_int[i + 1] - self.airfoil_x_coords_int[i])
                * 0.5
            )
            self.delta_area_array_int[i] = delta_area_int_i
        area_int = np.sum(self.delta_area_array_int)
        # área determinada pelo intradorso e a linha de corda

        self.area = area_ext - area_int
        # área do perfil

    def import_camber_line(self):

        np_array_x, np_array_y = import_airfoil_coordinates(self.name)
        x_interp = np.arange(0, 1, 0.02)
        minpos = np.argmin(np_array_x)
        # posição do menor valor no vetor de coordenadas horizontais,
        # determina a posição do bordo de ataque

        n = np_array_x.size
        # número de elementos do vetor de coordenadas horizontais

        np_array_x_ext = np_array_x[0:minpos]
        np_array_x_ext = np.flip(np_array_x_ext)
        # coordenadas horizontais do extradorso

        np_array_x_int = np_array_x[minpos: n - 1]
        # coordenadas horizontais do intradorso

        np_array_y_int = np_array_y[minpos: n - 1]
        # coordenadas verticais do intradorso

        np_array_y_ext = np_array_y[0:minpos]
        np_array_y_ext = np.flip(np_array_y_ext)
        # coordenadas verticais do extradorso

        y_interp_ext = np.interp(x_interp, np_array_x_ext, np_array_y_ext)
        y_interp_int = np.interp(x_interp, np_array_x_int, np_array_y_int)
        y_camber = (y_interp_int + y_interp_ext) / 2
        camber_line = pd.DataFrame({"x": x_interp, "y": y_camber})
        self.Camber_line = camber_line
