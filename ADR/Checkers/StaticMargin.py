class StaticMarginChecker:
    def __init__(self, plane):
        self.plane = plane
        self.SM_alpha = plane.SM_alpha

    def check(self):
        positive_alphas = self.SM_alpha[(self.SM_alpha.index > 0)]
        positive_sm = positive_alphas["SM"] > 0

        if positive_sm.all() == True:
            self.plane.positive_sm_for_positive_alphas = True
        else:
            self.plane.positive_sm_for_positive_alphas = False
            print(
                "This aircraft does *not* have positive Static Margin for all positive alphas!"
            )
