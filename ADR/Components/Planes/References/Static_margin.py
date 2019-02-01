import math

def toRad(graus):
    return graus * math.pi / 180

class SM:
    def __init__(self):
        self.SM = 0

    def set(self, CLW1, CDW1, index_w1, areaW1,
            CLW2, CDW2, index_w2, areaW2,
            CLT, CDT, index_t, areaT, incidenceT,
            W1_downwash_angle, eta, CM_alpha, alpha_p):

        den = (CLW1[index_w1] + CLW2[index_w2] * areaW2 / areaW1) * math.cos(toRad(alpha_p)) + \
              (CDW1[index_w1] + CDW2[index_w2] * areaW2 / areaW1) * math.sin(toRad(alpha_p)) + \
              (CLT[index_t] * math.cos(toRad(alpha_p) - W1_downwash_angle) +
               CDT[index_t] * math.sin(toRad(alpha_p) - W1_downwash_angle)) \
                * eta * areaT / areaW1

        self.SM = -CM_alpha / den
        # DEBUG

    #        print('\t\t\t ME calc:')
    #        print('\t\t\t index aw1 | clw1 | cdw1 | ind aw2 | clw2 | cdw2 | ind at | clt | cd t | ME' )
    #        print('\t\t\t {}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{} \
    #              '.format(index_w1,CLW1[index_w1],CDW1[index_w1],index_w2,CLW2[index_w2],CDW2[index_w2],\
    #                index_t,CLT[index_w1],CDT[index_w1],self.SM))

    def get(self):
        return self.SM