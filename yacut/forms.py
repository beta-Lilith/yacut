from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .models import MAX_SHORT_LENGTH

DATA_REQUIRED = 'Это обязательное поле'


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message=DATA_REQUIRED)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, MAX_SHORT_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
