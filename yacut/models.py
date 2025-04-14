import random
import re
from datetime import datetime

from flask import url_for

from settings import (ALLOWED_CHARS, ALLOWED_REGEXP, MAX_GEN_TRIES,
                      ORIGINAL_MAX_LENGTH, REDIRECT_VIEW, SHORT_AUTO_LENGTH,
                      SHORT_MAX_LENGTH)

from . import db
from .error_handlers import (NotUniqueShortError, OriginalLenError,
                             ShortLenError, ValidateShortError)

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL = 'Указано недопустимое имя для длинной ссылки'
NOT_UNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_short_url(self):
        return url_for(REDIRECT_VIEW, short=self.short, _external=True)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_unique_short():
        for _ in range(MAX_GEN_TRIES):
            short = ''.join(random.choices(ALLOWED_CHARS, k=SHORT_AUTO_LENGTH))
            if short != URLMap.get(short):
                return short

    @staticmethod
    def create(original, short=None, validate=True):
        if validate:
            if len(original) > ORIGINAL_MAX_LENGTH:
                raise OriginalLenError(INVALID_ORIGINAL)
            if short and len(short) > SHORT_MAX_LENGTH:
                raise ShortLenError(INVALID_SHORT)
            if short and not re.match(ALLOWED_REGEXP, short):
                raise ValidateShortError(INVALID_SHORT)
            if short and URLMap.get(short=short):
                raise NotUniqueShortError(NOT_UNIQUE_SHORT)
        if not short:
            short = URLMap.create_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
