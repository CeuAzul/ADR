class MaybeAnAssassin:
    def __init__(self, plane):
        self.plane = plane

    def score_or_kill(self):
        if (
            self.plane.trimm_for_low_angles
            and self.plane.trimm_for_high_angles
            and self.plane.positive_sm_for_positive_alphas
            and self.plane.dimensions_are_good
            and self.plane.mtow > 0
        ):

            self.plane.payload = self.plane.mtow - self.plane.dead_weight

            self.plane.score = 12.5 * self.plane.payload
            print("Plane is alive and scored {}".format(self.plane.score))
        else:
            self.plane.dead = True
            self.plane.score = 0
            print("Plane is dead")
