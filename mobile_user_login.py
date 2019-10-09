import random
from decrypt import *


class MobileUserLogin:
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
        self.bi = 'bio'

    def log_in(self, smart_car, service_index):
        P_1 = smart_car[1]
        P_2 = smart_car[2]
        rho_dot = P_1 ^ hash(self.bi + self.user_pw)
        # P_1 = hash(self.bi + self.user_pw) ^ self.rho

        if P_2 == hash(str(rho_dot) + self.bi + self.user_pw + str(self.user_id)):
            print('P2 is right')
        else:
            print('P2 is bad')
        NBPW = hash(str(hash(self.bi + str(self.user_id) + self.user_pw)) + str(rho_dot))
        # P_1 = hash(self.bi + self.user_pw) ^ self.rho
        # rho_dot = P_1 ^ hash(self.bi + self.user_pw)
        N_dot_index = smart_car[3][service_index - 1]
        self.M_ij = N_dot_index ^ NBPW
        self.RDN_i = random.getrandbits(128)
        Tm = 0000
        Z_1 = self.M_ij ^ hash(service_index) ^ Tm ^ self.RDN_i
        H_1 = hash(str(Z_1) + str(self.user_id) + str(Tm) + str(self.RDN_i))
        NId_cs_dot = smart_car[5][service_index - 1]
        NId_cs = NId_cs_dot ^ hash(str(rho_dot) + self.bi)
        AID_ij = smart_car[4][service_index - 1]
        N_dot = smart_car[3][service_index - 1]
        XId_U = AID_ij ^ hash(str(N_dot) + str(self.user_id))
        XId_U_star = XId_U ^ hash(str(Tm) + str(NId_cs))
        log_in_result = [Z_1, XId_U_star, Tm, H_1]
        return log_in_result

    def monile_authentiation(self, au_result, smart_car, service_index):
        Z_2 = au_result[0]
        get_access_policy = au_result[1]
        Tm = au_result[4]
        X_2 = Z_2 ^ self.M_ij ^ self.user_id ^ Tm
        ct = au_result[2]
        pk = smart_car[9]
        sk = smart_car[8][service_index - 1]
        groupObj = PairingGroup('SS512')
        cpabe = CPabe_BSW07(groupObj)
        rec_msg = cpabe.decrypt(pk, sk, ct)
        SKYu_i_s_j = hash(
            str(self.user_id) + str(service_index) + str(rec_msg) + str(self.M_ij) + str(self.RDN_i) + str(X_2) + str(Tm) + str(Tm))
        print('SKYu_i_s_j is {}'.format(SKYu_i_s_j))
        print('M_ij is {}'.format(self.M_ij))
        H_4 = hash(
            str(self.user_id) + get_access_policy + str(ct) + str(Tm) + str(self.RDN_i) + str(SKYu_i_s_j) + str(
                Tm) + str(X_2))
        H_3 = au_result[3]
        if H_3 == H_4:
            print('H_3 H_4 is fine')
        else:
            print('H_3 H_4 is bad')
