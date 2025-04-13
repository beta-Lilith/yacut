import re
import os
import string


ORIGINAL_MAX_LENGTH = 2048
SHORT_MAX_LENGTH = 16
SHORT_AUTO_LENGTH = 6

ALLOWED_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits
ALLOWED_REGEXP = f'^[{re.escape(ALLOWED_CHARS)}]*$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
