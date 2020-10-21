import pyotp
from .models import User


def is_unique(otp):
    try:
        User.objects.get(otp=otp)
    except User.DoesNotExist:
        return True
    return False


def generate_key():
    global totp
    otp = pyotp.random_base32()
    totp = pyotp.TOTP(otp, interval=300)
    password = totp.now()

    if is_unique(otp):
        return password
