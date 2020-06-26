"""
Origem: Bordo de ataque da asa raiz
"""

# Descobre o intervalo aceitavel de posicionamento do CG

from ADR.Components.References.Static_margin import SM
from ADR.Core.data_manipulation import dict_to_dataframe, find_df_roots


class FlightStability:
    def __init__(self, plane):
        self.plane = plane
        self.wing1 = self.plane.wing1
        # wing2 equals wing 1 for now (monoplane)
        self.wing2 = self.plane.wing2
        self.hs = self.plane.hs

        if self.plane.plane_type != "monoplane" and self.plane.plane_type != "biplane":
            print("Incapable of analysing FlightStability of this plane type")

        self.CM_plane_CG(plane.cg)
        self.static_margin()

    def CM_plane_CG(self, cg):

        CM_alpha_CG_tail = {}
        CM_alpha_CG_wing1 = {}
        CM_alpha_CG_wing2 = {}
        CM_alpha_CG_wings = {}
        CM_alpha_CG_plane = {}
        self.CM_alpha_CG_plane_each_hs_incidence = {}

        for alpha_plane in self.plane.alpha_range:

            self.wing1.update_alpha(float(alpha_plane))
            self.wing2.update_alpha(float(alpha_plane))

            # Getting CM_alpha of wing1
            CM_alpha_CG_wing1[alpha_plane] = self.wing1.moment_on_CG(
                self.wing1, self.plane.cg, alpha_plane
            )

            CM_alpha_CG_wings[alpha_plane] = CM_alpha_CG_wing1[alpha_plane]

            if self.plane.plane_type == "biplane":
                CM_alpha_CG_wing2[alpha_plane] = self.wing2.moment_on_CG(
                    self.wing1, self.plane.cg, alpha_plane
                )
                CM_alpha_CG_wings[alpha_plane] += CM_alpha_CG_wing2[alpha_plane]

        for hs_incidence in self.hs.incidence_range:
            self.hs.incidence = hs_incidence
            for alpha_plane in self.plane.alpha_range:
                self.hs.update_alpha(float(alpha_plane))

                if self.hs.attack_angle in self.hs.get_alpha_range():
                    # Getting CM_alpha of tail
                    CM_alpha_CG_tail[alpha_plane] = self.hs.moment_on_CG(
                        self.wing1, self.plane.cg, alpha_plane
                    )
                    # Summing CM of tail with CM of wing per each alpha
                    # Getting CM_alpha of plane
                    CM_alpha_CG_plane[alpha_plane] = (
                        CM_alpha_CG_wings[alpha_plane] +
                        CM_alpha_CG_tail[alpha_plane]
                    )
                else:
                    CM_alpha_CG_tail[alpha_plane] = None
                    CM_alpha_CG_plane[alpha_plane] = None

            CM_alpha_CG_plane_df = dict_to_dataframe(
                CM_alpha_CG_plane, "CM", "alpha")
            self.CM_alpha_CG_plane_each_hs_incidence[
                hs_incidence
            ] = CM_alpha_CG_plane_df

        self.trimm()

        dCM_dalpha_plane_df = self.CM_alpha_CG_plane_each_hs_incidence[0].diff(
        )
        dCM_dalpha_plane_df.fillna(method="bfill", inplace=True)
        self.plane.dCM_dalpha = dCM_dalpha_plane_df

        self.wing1.CM_alpha_CG = dict_to_dataframe(
            CM_alpha_CG_wing1, "CM", "alpha")
        self.wing2.CM_alpha_CG = dict_to_dataframe(
            CM_alpha_CG_wing2, "CM", "alpha")
        self.hs.CM_alpha_CG = dict_to_dataframe(
            CM_alpha_CG_tail, "CM", "alpha")

        return self.CM_alpha_CG_plane_each_hs_incidence

    def static_margin(self):
        SM_alpha = {}
        self.hs.incidence = 0
        for alpha_plane in self.plane.alpha_range:
            self.wing1.update_alpha(float(alpha_plane))
            self.wing2.update_alpha(float(alpha_plane))
            self.hs.update_alpha(float(alpha_plane))

            if self.hs.attack_angle in self.hs.get_alpha_range():
                # Calculating Static Margin for each alpha
                self.sm = SM(
                    self.plane.plane_type,
                    self.wing1,
                    self.wing2,
                    self.hs,
                    alpha_plane,
                    self.plane.dCM_dalpha.at[alpha_plane, "CM"],
                )  # TODO: We should pass the entire plane into SM analysys
                SM_alpha[alpha_plane] = self.sm.SM

        self.SM_alpha_df = dict_to_dataframe(SM_alpha, "SM", "alpha")
        self.plane.SM_alpha = self.SM_alpha_df
        return self.SM_alpha_df

    def trimm(self):
        tail_trimm = {}
        for hs_incidence in self.hs.incidence_range:
            root = find_df_roots(
                self.CM_alpha_CG_plane_each_hs_incidence[hs_incidence], "CM"
            )
            if len(root) != 0:
                alpha_trimm = root[0]
                tail_trimm[alpha_trimm] = hs_incidence

        self.tail_trimm = tail_trimm
        self.tail_trimm_df = dict_to_dataframe(
            tail_trimm, "hs_incidence", "alpha")
        self.plane.tail_trimm = self.tail_trimm_df

        if tail_trimm:
            self.plane.alpha_trimm_min = min(tail_trimm, key=tail_trimm.get)
            self.plane.alpha_trimm_max = max(tail_trimm, key=tail_trimm.get)
        else:
            self.plane.alpha_trimm_min = 0
            self.plane.alpha_trimm_max = 0

        return self.tail_trimm_df
