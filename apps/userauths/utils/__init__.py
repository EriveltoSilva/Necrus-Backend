import shortuuid

def generate_otp(length=12):
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]
