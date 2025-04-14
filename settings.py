import os
import re
import string

ORIGINAL_MAX_LENGTH = 2048
SHORT_MAX_LENGTH = 16
SHORT_AUTO_LENGTH = 6
MAX_GEN_TRIES = 100

ALLOWED_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits
ALLOWED_REGEXP = f'^[{re.escape(ALLOWED_CHARS)}]*$'

REDIRECT_VIEW = 'redirect_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
