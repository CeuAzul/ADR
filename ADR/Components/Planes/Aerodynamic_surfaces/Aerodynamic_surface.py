from ADR.Components.Planes.Points.CA import CA

class Aerodynamic_surface():
    def __init__(self, data):
        self.CA = CA()
        self.CL = data.get("CL")
        self.CD = data.get("CD")
        self.CM = data.get("CM")
        self.span = data.get("span")
        self.chord = data.get("chord")
        self.incidence = data.get("incidence")
        self.stall_min = data.get("stall_min")
        self.stall_max = data.get("stall_max")
        self.area = data.get("area")
        self.downwash_angle = data.get("downwash_angle")

        self.CA.setX(data.get("X_CA"))
        self.CA.setH(data.get("H_CA"))

    def setCA(self):
        pass
        #CA = CA()

    def drag(self):
        rho = 1
        V =  10
        C_D = 1
        Drag = 0.5*rho*V**2*self.area*C_D
        return Drag

    def lift(self):
        rho = 1
        V =  10
        C_L = 1
        Lift = 0.5*rho*V**2*self.area*C_L
        return Lift

    def moment(self):
        rho = 1
        V =  10
        C_M = 1
        Moment = 0.5*rho*V**2*self.area*C_M
        return Moment


#
