"""
Origem: Bordo de ataque da asa raiz
"""
import math


def toRad(graus):
    return graus * math.pi / 180


def wing_momentum(plane_type, wing1, wing2, cg, alpha_plane):

    item1 = wing1.CL_alpha.at[wing1.attack_angle, 'CL'] * math.cos(toRad(alpha_plane)) * (cg.x - wing1.CA.x) / wing1.chord1
    item2 = wing1.CL_alpha.at[wing1.attack_angle, 'CL'] * math.sin(toRad(alpha_plane)) * (cg.h - wing1.CA.h) / wing1.chord1
    item5 = wing1.CD_alpha.at[wing1.attack_angle, 'CD'] * math.sin(toRad(alpha_plane)) * (cg.x - wing1.CA.x) / wing1.chord1
    item6 = wing1.CD_alpha.at[wing1.attack_angle, 'CD'] * math.cos(toRad(alpha_plane)) * (cg.h - wing1.CA.h) / wing1.chord1
    CM = wing1.CM_alpha.at[wing1.attack_angle, 'CM'] + item1 + item2 + item5 - item6

    """print("\tDados wing1")
    print("\tCL = ", wing1.CL_alpha[index_w1])
    print("\tInclinação aviao (graus)= ", alpha_plane)
    print("\tInclinação aviao (rad)= ", toRad(alpha_plane))
    print("\tcg.x - CA1_X = ", cg.x - CA1_X)
    print("\tcg.h - CA1_H = ", (cg.h - CA1_H))
    print("\tItens = ", item1, item2, item5, item6)
    print("\tCM1 = ", CM1)
    print()"""

    if plane_type == "biplane":
        item3 = wing2.CL_alpha.at[wing2.attack_angle, 'CL'] * math.cos(toRad(alpha_plane)) * ((cg.x - wing2.CA.x) / wing1.chord1) * wing2.area / wing1.area
        item4 = wing2.CL_alpha.at[wing2.attack_angle, 'CL'] * math.sin(toRad(alpha_plane)) * ((cg.h - wing2.CA.h) / wing1.chord1) * wing2.area / wing1.area
        item7 = wing2.CL_alpha.at[wing2.attack_angle, 'CL'] * math.sin(toRad(alpha_plane)) * ((cg.x - wing2.CA.x) / wing1.chord1) * wing2.area / wing1.area
        item8 = wing2.CL_alpha.at[wing2.attack_angle, 'CL'] * math.cos(toRad(alpha_plane)) * ((cg.h - wing2.CA.h) / wing1.chord1) * wing2.area / wing1.area
        CM += wing2.CM_alpha.at[wing2.attack_angle, 'CM'] * (wing2.area * wing2.chord1) / (wing1.area * wing1.chord1) + item3 + item4 + item7 - item8
        return CM
    elif plane_type == "monoplane":
        return CM
    else:
        print("------ Error: Incapable of calculating resulting momentum of given plane ------")


def tail_momentum(wing1, hs, cg, alpha_plane):

    item9 = hs.CL_alpha[hs.attack_angle_index()] * math.cos(toRad(alpha_plane)) * (
            (cg.x - hs.CA.x) / wing1.chord1) * hs.area / wing1.area
    item10 = hs.CL_alpha[hs.attack_angle_index()] * math.sin(toRad(alpha_plane)) * (
            (cg.h - hs.CA.h) / wing1.chord1) * hs.area / wing1.area
    item11 = hs.CD_alpha[hs.attack_angle_index()] * math.cos(toRad(alpha_plane)) * (
            (cg.h - hs.CA.h) / wing1.chord1) * hs.area / wing1.area
    item12 = hs.CD_alpha[hs.attack_angle_index()] * math.sin(toRad(alpha_plane)) * (
            (cg.x - hs.CA.x) / wing1.chord1) * hs.area / wing1.area
    CM = (hs.CM_alpha * hs.chord1 * hs.area / (wing1.chord1 * wing1.area)) + item9 + item10 - item11 + item12

    """print("Dados EH")
    print("CL = ", CL[index_t])
    print("Inclinação profundor (graus)= ", alpha_plane)
    print("Inclinação profundor (rad)= ", toRad(alpha_plane))
    print("Incidence = ", incidence)
    print("cg.x - CA_X = ", cg.x - CA_X)
    print("", "Itens = ", item9, item10, item11, item12)
    print("CM = ", CM)

    print()"""

    return CM
