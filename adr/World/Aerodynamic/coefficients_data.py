def get_CL(angle_of_attack):
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 0
    else:
        return 0.6 + 0.1 * angle_of_attack


def get_CD(angle_of_attack):
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 10 * (0.06 + 0.01 * 15)
    else:
        return 0.06 + 0.01 * angle_of_attack


def get_CM(angle_of_attack):
    a = 0.0012365
    b = -0.016365
    c = -0.2327
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 0
    else:
        return a * angle_of_attack**2 + b * angle_of_attack + c


def get_CL_inv(angle_of_attack):
    angle_of_attack = -angle_of_attack
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 0
    else:
        return -1 * (0.6 + 0.1 * angle_of_attack)


def get_CD_inv(angle_of_attack):
    angle_of_attack = -angle_of_attack
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 10 * (0.06 + 0.01 * 15)
    else:
        return 0.06 + 0.01 * angle_of_attack


def get_CM_inv(angle_of_attack):
    angle_of_attack = -angle_of_attack
    a = 0.0012365
    b = -0.016365
    c = -0.2327
    if angle_of_attack > 15 or angle_of_attack < -5:
        return 0
    else:
        return -1 * (a * angle_of_attack**2 + b * angle_of_attack + c)
