import datetime
import string
import random

def get_order_code(length=12):
    code = str(datetime.datetime.now()).replace("-","").replace(" ","").replace(":","")
    code = code.split('.')[0]
    length = 4
    print(code)
    return code + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


#print(get_order_code())