class TrimmRangeChecker:
    def __init__(self, plane):
        self.plane = plane
        self.alpha_min_trimm = plane.alpha_trimm_min
        self.alpha_max_trimm = plane.alpha_trimm_max
        self.alpha_min_power = plane.alpha_min
        self.alpha_max_power = plane.alpha_max

        self.trimm_tolerance = 2

    def check(self):
        if abs(self.alpha_min_power + self.trimm_tolerance) <= abs(
            self.alpha_min_trimm
        ):
            self.plane.trimm_for_low_angles = True
        else:
            self.plane.trimm_for_low_angles = False
            print("This aircraft does *not* trimm for low angles!")

        if abs(self.alpha_max_power - self.trimm_tolerance) <= abs(
            self.alpha_max_trimm
        ):
            self.plane.trimm_for_high_angles = True
        else:
            self.plane.trimm_for_high_angles = False
            print("This aircraft does *not* trimm for high angles!")
