class Motor():
    def __init__(self):
        self.maxThrust= 235
        self.thrustByVelocity = range(1,10)
        
    def get_take_off_thrust(self):
        return self.thrustByVelocity[5]
