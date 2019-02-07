import math


def toRad(graus):
    return graus * math.pi / 180


class SM:
    def __init__(self, CLW1, CDW1, index_w1, alpha_w1, areaW1,
            CLW2, CDW2, index_w2, alpha_w2, areaW2,
            CLT, CDT, index_t, alpha_t, areaT, incidenceT,
            W1_downwash_angle, eta, CM):

        den = CLW1[index_w1] * math.cos(toRad(alpha_w1)) * areaW2 / areaW1 \
              + CDW1[index_w1] * math.sin(toRad(alpha_w1)) * areaW2 / areaW1 \
              + CLW2[index_w2] * math.cos(toRad(alpha_w2)) * areaW2 / areaW1 \
              + CDW2[index_w2] * math.sin(toRad(alpha_w2)) * areaW2 / areaW1 \
              + CLT[index_t] * math.cos(toRad(alpha_t + W1_downwash_angle - incidenceT)) \
              + CDT[index_t] * math.sin(toRad(alpha_t + W1_downwash_angle - incidenceT)) \
              * eta * areaT / areaW1

        self.SM = -CM / den

