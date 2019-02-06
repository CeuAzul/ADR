import os
import pandas as pd
import numpy as np
import pkg_resources
import ADR

class Airfoil:
    def __init__(self, data):
        self.name = data.get("airfoil")
        self.import_aerodynamic_data()
        # get coordinates from airfoil name and airfoil folder / pandas
        self.generate_upper_surface_coordinates()
        self.generate_inner_surface_coordinates()
        self.calc_thickness()
        self.calc_perimeter()
        self.calc_area()

    def import_aerodynamic_data(self):
        package_filepath = ADR.__file__.replace('__init__.py', '')
        airfoil_aerodynamic_data_filename = 'xf-' + self.name + '-il-200000.csv'
        airfoil_aerodynamic_data_filepath = package_filepath + 'World/Profiles/AerodynamicData/' + airfoil_aerodynamic_data_filename

        airfoil_df = pd.read_csv(airfoil_aerodynamic_data_filepath, skiprows=10, index_col=0)
        self.Cl_alpha = airfoil_df[["Cl"]]
        self.Cd_alpha = airfoil_df[["Cd"]]
        self.Cm_alpha = airfoil_df[["Cm"]]

    def import_coordinates(self):
        # TODO: Jonny is going to put his coordinates code here
        pass

    def get_Cl(self, alpha):
        Cl = np.interp(alpha, self.Cl_alpha.index.values, self.Cl_alpha['Cl'])
        return Cl

    def get_Cd(self, alpha):
        Cd = np.interp(alpha, self.Cd_alpha.index.values, self.Cd_alpha['Cd'])
        return Cd

    def get_Cm(self, alpha):
        Cm = np.interp(alpha, self.Cm_alpha.index.values, self.Cm_alpha['Cm'])
        return Cm

    def generate_upper_surface_coordinates(self):
        # TODO: Jonny is going to put his intradorso code here
        pass

    def generate_inner_surface_coordinates(self):
        # TODO: Jonny is going to put his extradorso code here
        pass

    def calc_thickness(self):
        # TODO: Jonny is going to put his thickness code here
        pass

    def calc_perimeter(self):
        # TODO: Jonny is going to put his perimeter code here
        pass

    def calc_area(self):
        # TODO: Jonny is going to put his area code here
        pass
