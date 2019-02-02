class Motor():
    def __init__(self, static_thrust, linear_decay_coefficient):
        self.static_thrust = static_thrust
        self.linear_decay_coefficient = linear_decay_coefficient

    def thrust(self, velocity):
        thrust = self.static_thrust - self.linear_decay_coefficient*velocity
        return thrust