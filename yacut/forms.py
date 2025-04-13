from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Regexp, Optional

from settings import ALLOWED_REGEXP, ORIGINAL_MAX_LENGTH, SHORT_MAX_LENGTH

ORIGINAL_COMMENT = 'Длинная ссылка'
SHORT_COMMENT = 'Ваш вариант короткой ссылки'
DATA_REQUIRED = 'Это обязательное поле'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_COMMENT,
        validators=[
            Length(max=ORIGINAL_MAX_LENGTH),
            DataRequired(message=DATA_REQUIRED)
        ]
    )
    custom_id = URLField(
        SHORT_COMMENT,
        validators=[
            Length(max=SHORT_MAX_LENGTH),
            Optional(),
            Regexp(ALLOWED_REGEXP, message=INVALID_SHORT)
        ]
    )
    submit = SubmitField('Создать')
