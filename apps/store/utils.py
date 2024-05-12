import shortuuid

def generate_session_id(length=12):
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]

def print_debug(message):
    print("#"*100)
    print(f"{message}".center(100))
    print("#"*100)