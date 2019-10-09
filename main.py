from mobile_user_register import *
from registration_center import *
from mobile_user_login import *
from cloud_service_provider import *

# init
register = RegistrationCenter()
register.initation()

mobile_register = MobileUserRegister(12, '123')
NBPW_result = mobile_register.NBPW_gen()
user_id = NBPW_result[0]
NBPW = NBPW_result[1]

smart_car_result = register.smart_car(user_id, NBPW)
smart_car = mobile_register.smart_car_save(smart_car_result)

mobile_login = MobileUserLogin(12, '123')
log_in_result = mobile_login.log_in(smart_car, 1)

cloudProvider = CloudServiceProvider()
PK = smart_car[9]
au_result = cloudProvider.authentication(log_in_result, 1, register, PK)
mobile_login.monile_authentiation(au_result, smart_car, 1)


