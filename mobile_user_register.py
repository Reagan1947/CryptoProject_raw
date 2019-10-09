# -*-coding:utf8-*-
import random


class MobileUserRegister:
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
        self.rho = random.getrandbits(128)
        self.m = random.getrandbits(128)
        self.bi = 'bio'

    def NBPW_gen(self):
        NBPW = hash(str(hash(self.bi + str(self.user_id) + self.user_pw)) + str(self.rho))
        NBPW_result = [self.user_id, self.m ^ NBPW]
        return NBPW_result

    def smart_car_save(self, smart_car_result):
        P_1 = hash(self.bi + self.user_pw) ^ self.rho
        P_2 = hash(str(self.rho) + self.bi + self.user_pw + str(self.user_id))
        N_01 = smart_car_result[1][0][1]
        N_02 = smart_car_result[1][1][1]
        # N_01 = M_01 ^ NBPW
        N_dot_01 = N_01 ^ self.m
        N_dot_02 = N_02 ^ self.m
        AID_01 = smart_car_result[0] ^ hash(str(N_dot_01) + str(self.user_id))
        AID_02 = smart_car_result[0] ^ hash(str(N_dot_02) + str(self.user_id))
        NId_cs_01 = smart_car_result[1][0][2]
        NId_cs_02 = smart_car_result[1][1][2]
        NId_cs_01_dot = NId_cs_01 ^ hash(str(self.rho) + self.bi)
        NId_cs_02_dot = NId_cs_02 ^ hash(str(self.rho) + self.bi)

        ID_s = [1, 2]
        attrs_01 = smart_car_result[1][0][3]
        attrs_02 = smart_car_result[1][1][3]
        sk_01 = smart_car_result[1][0][4]
        sk_02 = smart_car_result[1][1][4]
        attrs = [attrs_01, attrs_02]
        sk = [sk_01, sk_02]
        N_dot = [N_dot_01, N_dot_02]
        AID = [AID_01, AID_02]
        NId_cs_dot = [NId_cs_01_dot, NId_cs_02_dot]
        pk = smart_car_result[2]

        smart_car = [self.bi, P_1, P_2, N_dot, AID, NId_cs_dot, ID_s, attrs, sk, pk]
        return smart_car
