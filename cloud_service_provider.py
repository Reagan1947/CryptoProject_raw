import sqlite3
import random
from charm.toolbox.pairinggroup import GT


class CloudServiceProvider:
    def authentication(self, log_in_result, service_index, register, PK):
        service_key = ''
        pair_key = ''
        user_id = ''
        abe_pk = ''
        data_base = 'service_0' + str(service_index) + '.db'
        conn = sqlite3.connect(data_base)
        c = conn.cursor()
        cursor = c.execute("SELECT service_key FROM main.base_information")
        for row_1 in cursor:
            service_key = row_1[0]
        NId_cs = hash(str(service_index) + service_key)
        XId_U_star = log_in_result[1]
        Tm = log_in_result[2]
        XId_U = XId_U_star ^ hash(str(NId_cs) + str(Tm))
        #################################### user id selet*???????????????
        record = c.execute('SELECT * FROM authentica_information')
        for row_2 in record:
            user_id = row_2[0]
            user_fake_id = row_2[1]
            pair_key = row_2[2]
        Q_ij = hash(str(hash(int(pair_key) ^ int(user_id))) + str(service_key))
        Z_1 = log_in_result[0]
        # service_index 是否str
        X_1 = Z_1 ^ hash(service_index) ^ Tm ^ Q_ij
        H_2 = hash(str(Z_1) + str(user_id) + str(Tm) + str(X_1))
        H_1 = log_in_result[3]

        if H_1 == H_2:
            print('H is fine')
        else:
            print('H is bad')

        rand_msg = register.groupObj.random(GT)
        access_policy_01 = '((four or three) and (three or one))'
        access_policy_02 = '((four or three) and (three or one))'
        access_policy = [access_policy_01, access_policy_02]
        get_access_policy = access_policy[service_index]
        cpabe = register.cpabe

        # pk = c.execute('SELECT pk FROM main.base_information')
        # for p in pk:
        #     abe_pk = p[0]

        ct = cpabe.encrypt(PK, rand_msg, get_access_policy)
        RDN_j = random.getrandbits(128)
        Z_2 = Q_ij ^ Tm ^ RDN_j ^ user_id
        SKY_s_j_U_i = hash(
            str(user_id) + str(service_index) + str(rand_msg) + str(Q_ij) + str(X_1) + str(RDN_j) + str(Tm) + str(Tm))
        print('Q_ij is {}'.format(Q_ij))
        print('SKY_s_j_U_i is {}'.format(SKY_s_j_U_i))
        H_3 = hash(
            str(user_id) + get_access_policy + str(ct) + str(Tm) + str(X_1) + str(SKY_s_j_U_i) + str(Tm) + str(RDN_j))
        au_result = [Z_2, get_access_policy, ct, H_3, Tm]
        return au_result
