from math import radians, cos, sin


class SM:
    """Class used to calculate the static margin
     for a given plane flying on a given alpha"""

    def __init__(self, plane_type, wing1, wing2, hs, alpha_plane, CM):

        self.SM = 0

        eta = 0.9
        den = (
            wing1.dCL_dalpha.at[wing1.attack_angle, "CL"] * cos(radians(alpha_plane))
            + wing1.dCD_dalpha.at[wing1.attack_angle, "CD"] * sin(radians(alpha_plane))
            + (
                hs.dCL_dalpha.at[hs.attack_angle, "CL"] * cos(radians(alpha_plane))
                + hs.dCD_dalpha.at[hs.attack_angle, "CD"] * sin(radians(alpha_plane))
            )
            * eta
            * hs.area
            / wing1.area
        )

        if plane_type == "biplane":
            den += (
                wing2.dCL_dalpha.at[wing2.attack_angle, "CL"]
                * cos(radians(alpha_plane))
                * wing2.area
                / wing1.area
                + wing2.dCD_dalpha.at[wing2.attack_angle, "CD"]
                * sin(radians(alpha_plane))
                * wing2.area
                / wing1.area
            )
            self.SM = (
                -CM / den
            )  # Colocar a corda media aerodinamica e nao a chorda da raiz.
        elif plane_type == "monoplane":
            self.SM = (
                -CM / den
            )  # Colocar a corda media aerodinamica e nao a chorda da raiz.
        else:
            print(
                "------ Error: Incapable of analysing Static Margin of given plane ------"
            )
