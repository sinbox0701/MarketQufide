import string
import random


def get_random_code(length=12):
    length = 16
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

print(get_random_code())
