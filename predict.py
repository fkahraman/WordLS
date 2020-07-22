"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""

from setup_Encoding import Admin
import time

############## CONFIG ##############

MODEL_TYPE = None # None or keras

############## CONFIG ##############

if __name__ == '__main__':

    admin = Admin()

    start = time.time()

    liste = ["kirap", 'armot', '1kolem', 'baharot', 'şiker', 'şikey', 'ayıncak', 'oyuncek', 'sosis']

    ct = 0
    for index in liste:

        out = admin.mode.predict(index, model_type=MODEL_TYPE)
        availalbe = admin.mode.predict_available(index, out)

        if availalbe:
            print(ct, '. ' + index + " -->", out, ' - ', 'Geçerli')

        else:
            print (ct, '. ' + index + " -->", out, ' - ', 'Geçersiz')

        ct += 1

    stop = time.time()

    print('Topalam süre: ',round(stop - start, 3))
