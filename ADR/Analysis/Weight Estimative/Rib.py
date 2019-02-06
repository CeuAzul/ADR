class Rib():
    def __init__(self, data):
        self.chord = data.get("chord")
        self.perimeter = data.get("perimeter")
        self.area = data.get("area")
        self.thickness = data.get("thickness")
        self.material = data.get("material")
        self.mass = data.get("mass")
        self.span_position = data.get("span_position")
        self.aerodynamic_id = data.get("aerodynamic_id")
        self.is_connection = data.get("is_connection")