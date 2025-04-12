import random
import string


ALLOWED_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits
URL_LENGTH = 6


def get_unique_short_id():
    return ''.join(random.choice(ALLOWED_CHARS) for _ in range(URL_LENGTH))


def valid_short_id(short_id):
    for char in short_id:
        if char not in ALLOWED_CHARS:
            return False
    return True
