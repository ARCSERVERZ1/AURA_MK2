import random, string

value = '105'

import random


def encrypt_value(value):
    x = 0
    rand = str(random.randint(1000000, 9999999))
    rand = [i for i in rand]
    for index, digit in enumerate(rand):
        if index in [2, 5, 8]:
            rand.insert(index, str(value)[x])
            x = x + 1
    return ''.join([i for i in rand])


print(encrypt_value(119))
