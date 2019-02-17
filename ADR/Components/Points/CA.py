from ADR.Components.Component import Component


class CA(Component):
    def __init__(self, data):
        super().__init__(data)

        self.abs_x = data.get("surface_x") + data.get("x")
        self.abs_z = data.get("surface_z") + data.get("z")
