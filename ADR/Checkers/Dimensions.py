class Ruler:
    def __init__(self, plane):
        self.plane = plane

    def measure(self):
        wing1_span = 2 * (self.plane.wing1.span1 + self.plane.wing1.span2)
        wing2_span = 2 * (self.plane.wing2.span1 + self.plane.wing2.span2)
        hs_span = 2 * (self.plane.hs.span1 + self.plane.hs.span2)
        y_max = max(wing1_span, wing2_span, hs_span)
        x_max = self.plane.motor.x - self.plane.hs.x + self.plane.hs.chord1
        total_dimension = y_max + x_max
        self.plane.total_dimensions = total_dimension

        if total_dimension < 3.71:
            self.plane.dimensions_are_good = True
        else:
            self.plane.dimensions_are_good = False
            print(
                "Plane is *outside* the dimensions. Total: {}".format(
                    self.plane.total_dimensions
                )
            )
