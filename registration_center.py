# -*-coding:utf8-*-
import random
from abenc_bsw07 import *
import sqlite3


class RegistrationCenter:
    def __init__(self):
        self.groupObj = PairingGroup('SS512')
        self.cpabe = CPabe_BSW07(self.groupObj)
        (self.pk, self.mk) = self.cpabe.setup()

    def initation(self):
        # Xij key #############################
        cs_secret_key = [random.getrandbits(1024), random.getrandbits(1024)]

        # service use the pk mk attrs get sk and enc it
        # sk = cpabe.keygen(pk, mk, attrs)
        conn_01 = sqlite3.connect('service_01.db')
        conn_02 = sqlite3.connect('service_02.db')
        c_01 = conn_01.cursor()
        c_02 = conn_02.cursor()
        PK = str(self.pk)
        MK = str(self.mk)
        service_key_01 = str(cs_secret_key[0])
        service_key_02 = str(cs_secret_key[1])
        c_01.execute('insert into main.base_information (service_id, service_key, pk, mk) '
                     'values ("{}", "{}", "{}", "{}")'.format(1, service_key_01, PK, MK))
        c_02.execute('insert into main.base_information (service_id, service_key, pk, mk) '
                     'values ("{}", "{}", "{}", "{}")'.format(1, service_key_02, PK, MK))

        conn_01.commit()
        conn_01.close()
        conn_02.commit()
        conn_02.close()

    def smart_car(self, user_id, mNBPW):
        global service_key_01, service_key_02
        pair_key_01 = random.getrandbits(1024)
        pair_key_02 = random.getrandbits(1024)
        conn_01 = sqlite3.connect('service_01.db')
        conn_02 = sqlite3.connect('service_02.db')
        c_01 = conn_01.cursor()
        c_02 = conn_02.cursor()
        cursor_01 = c_01.execute("SELECT service_key  from main.base_information")
        for row_01 in cursor_01:
            service_key_01 = row_01[0]
        cursor_02 = c_02.execute("SELECT service_key  from main.base_information")
        for row_02 in cursor_02:
            service_key_02 = row_02[0]

        c_01.execute("insert into main.authentica_information(user_id, user_fake_id, pair_key) "
                     "values (\"{}\", \"{}\", \"{}\")".format(user_id, user_id + 200, str(pair_key_01)))
        c_02.execute("insert into main.authentica_information(user_id, user_fake_id, pair_key) "
                     "values (\"{}\", \"{}\", \"{}\")".format(user_id, user_id + 200, str(pair_key_02)))

        conn_01.commit()
        conn_02.commit()
        conn_01.close()
        conn_02.close()
        M_01 = hash(str(hash(int(pair_key_01) ^ int(user_id))) + str(service_key_01))
        M_02 = hash(str(hash(pair_key_02 ^ user_id)) + str(service_key_02))
        N_01 = M_01 ^ mNBPW
        N_02 = M_02 ^ mNBPW
        NId_cs_01 = hash(str(1) + service_key_01)
        NId_cs_02 = hash(str(2) + service_key_02)
        # user temple_id ##############################################
        temple_user_id = user_id + 200
        #
        attrs_01 = ['ONE', 'TWO', 'THREE']
        attrs_02 = ['ONE', 'TWO', 'THREE']
        sk_01 = self.cpabe.keygen(self.pk, self.mk, attrs_01)
        sk_02 = self.cpabe.keygen(self.pk, self.mk, attrs_02)
        service_result_01 = [1, N_01, NId_cs_01, attrs_01, sk_01]
        service_result_02 = [2, N_02, NId_cs_02, attrs_02, sk_02]
        sr = [service_result_01, service_result_02]
        smart_car_result = [temple_user_id, sr, self.pk]

        return smart_car_result

        # base information
        # service id, service_key , master_key, master_public_key

