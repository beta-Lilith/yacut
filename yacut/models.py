from datetime import datetime
import random
import re

from flask import url_for

from . import db
from .error_handlers import (
    NotUniqueShortError,
    ShortLenError,
    ValidateShortError
)
from settings import (
    ALLOWED_CHARS,
    ALLOWED_REGEXP,
    SHORT_AUTO_LENGTH,
    ORIGINAL_MAX_LENGTH,
    SHORT_MAX_LENGTH
)

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
NOT_UNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_short_url(self):
        return url_for('redirect_view', short=self.short, _external=True)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    @staticmethod
    def get_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_unique_short():
        while True:
            short = ''.join(random.choices(ALLOWED_CHARS, k=SHORT_AUTO_LENGTH))
            if short != URLMap.get_short(short):
                break
        return short

    @staticmethod
    def validate_short(short):
        return re.match(ALLOWED_REGEXP, short) is not None

    @staticmethod
    def create(original, short=None):
        if not short:
            short = URLMap.create_unique_short()
        if len(short) > SHORT_MAX_LENGTH:
            raise ShortLenError(INVALID_SHORT)
        if not URLMap.validate_short(short):
            raise ValidateShortError(INVALID_SHORT)
        if URLMap.get_short(short=short):
            raise NotUniqueShortError(NOT_UNIQUE_SHORT)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
