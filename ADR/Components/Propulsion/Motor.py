from ADR.Components.Component import Component


class Motor(Component):
    def __init__(self, data):
        super().__init__(data)

        self.static_thrust = data.get("static_thrust")
        self.linear_decay_coefficient = data.get("linear_decay_coefficient")

    def thrust(self, velocity):
        thrust = self.static_thrust - self.linear_decay_coefficient * velocity
        return thrust
