"""
Origem: Bordo de ataque da asa raiz
"""
import math


def toRad(graus):
    return graus * math.pi / 180


def wing_momentum(plane_type, X_CG, H_CG,
                  CL1, CD1, CM_CA_W1, index_w1, chord1, area1, CA1_X, CA1_H,
                  CL2, CD2, CM_CA_W2, index_w2, chord2, area2, CA2_X, CA2_H,
                  alpha_plane):
    # Onde tem cosseno e seno é alfa plane

    item1 = CL1[index_w1] * math.cos(toRad(alpha_plane)) * (X_CG - CA1_X) / chord1
    item2 = CL1[index_w1] * math.sin(toRad(alpha_plane)) * (H_CG - CA1_H) / chord1
    item5 = CD1[index_w1] * math.sin(toRad(alpha_plane)) * (X_CG - CA1_X) / chord1
    item6 = CD1[index_w1] * math.cos(toRad(alpha_plane)) * (H_CG - CA1_H) / chord1
    CM1 = CM_CA_W1 + item1 + item2 + item5 - item6

    print("Dados Wing1")
    print("CL = ", CL1[index_w1])
    print("alpha_graus = ", alpha_plane)
    print("alpha_rad = ", toRad(alpha_plane))
    print("cos alpha_rad = ", math.cos(toRad(alpha_plane)))
    print("X_CG - CA1_X", X_CG - CA1_X)
    print("Itens", item1, item2, item5, item6)
    print("CM1", CM1)
    print()

    if plane_type == 'biplane':
        item3 = CL2[index_w2] * math.cos(toRad(alpha_plane)) * ((X_CG - CA2_X) / chord1) * area2 / area1
        item4 = CL2[index_w2] * math.sin(toRad(alpha_plane)) * ((H_CG - CA2_H) / chord1) * area2 / area1
        item7 = CD2[index_w2] * math.sin(toRad(alpha_plane)) * ((X_CG - CA2_X) / chord1) * area2 / area1
        item8 = CD2[index_w2] * math.cos(toRad(alpha_plane)) * ((H_CG - CA2_H) / chord1) * area2 / area1
        CM2 = (CM_CA_W2) * (area2 * chord2) / (area1 * chord1) + item3 + item4 + item7 - item8

        return CM1 + CM2

    elif plane_type == 'monoplane':
        return CM1
    else:
        print("------ Error: Incapaz de analisar aviao requisitado ------")


def tail_momentum(X_CG, H_CG,
                  CL, CD, CM_CA, index_t, chord, area, incidence,
                  CA_X, CA_H,
                  wing1_chord, wing1_area, wing1_downwash_angle,
                  alpha_plane):
    #   onde tem cosseno e seno é alfa plane - donwash, onde tem CL e CD é alfa T

    item9 = CL[index_t] * math.cos(toRad(alpha_plane) - wing1_downwash_angle) * (
            (X_CG - CA_X) / wing1_chord) * area / wing1_area
    item10 = CL[index_t] * math.sin(toRad(alpha_plane) - wing1_downwash_angle) * (
            (H_CG - CA_H) / wing1_chord) * area / wing1_area
    item11 = CD[index_t] * math.cos(toRad(alpha_plane) - wing1_downwash_angle) * (
            (H_CG - CA_H) / wing1_chord) * area / wing1_area
    item12 = CD[index_t] * math.sin(toRad(alpha_plane) - wing1_downwash_angle) * (
            (X_CG - CA_X) / wing1_chord) * area / wing1_area
    CM = (CM_CA * chord * area / (wing1_chord * wing1_area)) + item9 + item10 - item11 + item12

    print("\tDados EH")
    print("\tCL = ", CL[index_t])
    print("\talpha_graus = ", alpha_plane)
    print("\talpha_rad = ", toRad(alpha_plane))
    print("\tcos alpha_rad = ", math.cos(toRad(alpha_plane)))
    print("\tX_CG - CA_X = ", X_CG - CA_X)
    print("\t", "Itens = ", item9, item10, item11, item12)
    print("\tCM = ", CM)
    print()

    return CM