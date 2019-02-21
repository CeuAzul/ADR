class Boom():
    def __init__(self, plane_data, mass_data):
        self.rho_balse = mass_data.get("rho_balse")
        self.thickness_balse = mass_data.get("thickness_balse")
        self.wing1_chord1 = plane_data.get("wing1_chord1")
        self.wing1_x = plane_data.get("wing1_x")
        self.hs_x = plane_data.get("hs_x")
        self.get_weight()

    # O seguinte código retorna o dimensionamento de um boom em viga-caixão de seção quadrada 8cmx8cm de madeira balsa
    #engastado no bordo de fuga da asa
    def get_weight(self):

    # PROPRIEDADES DOS MATERIAIS #
        number_ribs = 4 #m

    # GEOMETRIAS DO AVIÃO #
        width_boom = 0.08 #m

    # CONTAS #
        length_boom = self.wing1_x - self.wing1_chord1 - self.hs_x

        volume_boom = (width_boom**2 - (width_boom - 2*self.thickness_balse)**2)*length_boom
        weight_ribs = number_ribs*width_boom**2*self.thickness_balse*self.rho_balse
        weight_boom = self.rho_balse*volume_boom + weight_ribs
        self.weight = weight_boom
        return weight_boom