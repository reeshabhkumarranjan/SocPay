import pyotp
from datetime import datetime
import hashlib
from random import randint

def getOTP():

    sysotp = pyotp.TOTP('base32secret3232')
    sysotp = int(sysotp.now())
    time = datetime.now()
    time = str(time)
    hash = hashlib.sha3_512(time.encode('utf-8')).hexdigest()
    value = int(hash,16)

    mod = value%100

    while(len(str(mod))!=6):
        s = str(mod)
        s += str(randint(1,9))
        mod = int(s)

    mod ^= sysotp

    while (len(str(mod)) != 6):
        s = str(mod)
        s += str(randint(1, 9))
        mod = int(s)

    return mod

def execute_transaction(user_from, user_to, amount):
    Transaction.objects.create(transaction_user_1 = user_from, transaction_user_2=user_to, transaction_amount=amount, transaction_accepted=True)