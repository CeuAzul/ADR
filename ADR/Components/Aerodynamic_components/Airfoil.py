import os
import pandas as pd
import numpy as np
import pkg_resources
import ADR

class Airfoil:
    def __init__(self, data):
        self.name = data.get("airfoil")
        self.import_aerodynamic_data()
        self.import_coordinates()
        self.generate_upper_surface_coordinates()
        self.generate_inner_surface_coordinates()
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
        
        # Aqui o arquivo de coordenadas no formato de arquivo de texto, conforme copiado e colado de um banco de dados é lido e editado
        #removendo espaços em branco adicionais para facilitar a separação em data frames. O formato do arquivo de coordenadas deve ser
        #o formato selig.
    
        package_filepath = ADR.__file__.replace('__init__.py', '')
        airfoil_coordinates_filename = self.name + '.dat'
        airfoil_coordinates_filepath = package_filepath + 'World/Profiles/Coordinates/' + airfoil_coordinates_filename
        file1 = open(airfoil_coordinates_filepath, "r")
        file2 = open(airfoil_coordinates_filepath.replace('.dat', '_edited.dat'), "wt")
        file2.write('x y \n')
        for line in file1: 
            file2.write(' '.join(line.split()) + '\n')
        file1.close()
        file2.close()
        
        #-----Criação do dataframe e transformação de dataframe em vetores (listas)-----
        # A partir do arquivo de texto é criado o dataframe com as coordenadas dos pontos do perfil. Esse dataframe é separado em coordendas
        #horizontais e verticais e em seguida transformados em vetores (listas).

        df = pd.read_csv(airfoil_coordinates_filepath.replace('.dat', '_edited.dat'), sep=' ', skiprows=[1])
        df_array_x = df.loc[:, 'x']
        df_array_y = df.loc[:, 'y']
        self.np_array_x = df_array_x.values #vetor de coordenadas horizontais
        self.np_array_y = df_array_y.values #vetor de coordenadas verticais        
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
        
        self.n = self.np_array_x.size #número de elementos do vetor de coordenadas horizontais
        self.minpos = np.argmin(self.np_array_x) #posição do menor valor no vetor de coordenadas horizontais, determina a posição do bordo de ataque
        self.np_array_x_ext = np.flip(self.np_array_x[0:self.minpos]) #coordenadas horizontais do extradorso
        self.np_array_y_ext = np.flip(self.np_array_y[0:self.minpos]) #coordenadas verticais do extradorso
        self.n_ext = self.np_array_x_ext.size #número de elementos do vetor de coordenadas horizontais do extradorso

    def generate_inner_surface_coordinates(self):
        
        self.np_array_x_int = self.np_array_x[self.minpos:self.n-1] #coordenadas horizontais do intradorso
        self.np_array_y_int = self.np_array_y[self.minpos:self.n-1] #coordenadas verticais do intradorso
        self.n_int = self.np_array_x_int.size #número de elementos do vetor de coordenadas horizontais do intradorso

    def calc_perimeter(self):
        
        self.delta_perimeter_array_ext = np.empty([self.n_ext-1]) #vetor contando as parcelas de perimetro do extradorso
        self.delta_perimeter_array_int = np.empty([self.n_int-1]) #vetor contando as parcelas de perimetro do intradorso
        for i in range (0,self.n_ext-2):
            delta_perimeter_i_ext = ((self.np_array_x_ext[i+1] - self.np_array_x_ext[i])**2 + (self.np_array_y_ext[i+1] - self.np_array_y_ext[i])**2)**0.5
            self.delta_perimeter_array_ext[i] = delta_perimeter_i_ext
        perimeter_ext = np.sum(self.delta_perimeter_array_ext) #perímetro do extradorso do perfil
        for i in range (0,self.n_int-2):
            delta_perimeter_i_int = ((self.np_array_x_int[i+1] - self.np_array_x_int[i])**2 + (self.np_array_y_int[i+1] - self.np_array_y_int[i])**2)**0.5
            self.delta_perimeter_array_int[i] = delta_perimeter_i_int
        perimeter_int = np.sum(self.delta_perimeter_array_int) #perímetro do intradorso do perfil
        self.perimeter = perimeter_ext + perimeter_int #perimetro total do perfil
        print(self.perimeter)
        
        self.sum_perimeter_ext_pos = np.empty([self.n_ext-1])
        sum_perimeter_ext_pos_i = 0
        for i in range (0, self.n_ext-2):
            sum_perimeter_ext_pos_i = sum_perimeter_ext_pos_i + self.delta_perimeter_array_ext[i]
            self.sum_perimeter_ext_pos[i] = sum_perimeter_ext_pos_i

        self.sum_perimeter_int_pos = np.empty([self.n_int-1])
        sum_perimeter_int_pos_i = 0
        for i in range (0,self.n_int-2):
            sum_perimeter_int_pos_i = sum_perimeter_int_pos_i + self.delta_perimeter_array_int[i]
            self.sum_perimeter_int_pos[i] = sum_perimeter_int_pos_i
        
    def calc_area(self):
        
        self.delta_area_array_ext = np.empty([self.n_ext-1]) #vetor contando as parcelas de área determinadas pelo extradordo e a linha de corda
        self.delta_area_array_int = np.empty([self.n_int-1]) #vetor contando as parcelas de área determinadas pelo intradordo e a linha de corda
        for i in range (0,self.n_ext-2):
            delta_area_ext_i = ((self.np_array_y_ext[i] + self.np_array_y_ext[i+1]) * (self.np_array_x_ext[i+1] - self.np_array_x_ext[i]) * 0.5)
            self.delta_area_array_ext[i] = delta_area_ext_i  
        area_ext = np.sum(self.delta_area_array_ext) #área determinada pelo extradordo e a linha de corda
        for i in range (0,self.n_int-2):
            delta_area_int_i = ((self.np_array_y_int[i] + self.np_array_y_int[i+1]) * (self.np_array_x_int[i+1] - self.np_array_x_int[i]) * 0.5)
            self.delta_area_array_int[i] = delta_area_int_i   
        area_int = np.sum(self.delta_area_array_int) #área determinada pelo intradorso e a linha de corda
        self.area = area_ext - area_int #área do perfil
        print(self.area)
