import math


def toRad(graus):
    return graus * math.pi / 180


class SM:
    def __init__(self, plane_type, wing1, wing2, hs,
                 alpha_plane,
                 CM):

        self.SM = 0

        eta = 0.9
        den = wing1.dCL_dalpha[wing1.attack_angle_index()] * math.cos(toRad(alpha_plane))\
              + wing1.dCD_dalpha[wing1.attack_angle_index()] * math.sin(toRad(alpha_plane))\
              + (hs.dCL_dalpha[hs.attack_angle_index()] * math.cos(toRad(alpha_plane))
              + hs.dCD_dalpha[hs.attack_angle_index()] * math.sin(toRad(alpha_plane)))\
              * eta * hs.area / wing1.area

        if plane_type == "biplane":
            den += wing2.dCL_dalpha[wing2.attack_angle_index()] * math.cos(toRad(alpha_plane)) * wing2.area / wing1.area \
                + wing2.dCD_dalpha[wing2.attack_angle_index()] * math.sin(toRad(alpha_plane)) * wing2.area / wing1.area
            self.SM = -CM / den
        elif plane_type == "monoplane":
            self.SM = -CM / den
        else:
            print("------ Error: Incapable of analysing Static Margin of given plane ------")
