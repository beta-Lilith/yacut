from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id, valid_short_id


NOT_UNIQUE_SHORT_ID = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), 200
    short_id = (
        form.custom_id.data
        if form.custom_id.data
        else get_unique_short_id()
    )
    if not valid_short_id(short_id):
        flash(INVALID_SHORT_ID)
        return render_template('index.html', form=form), 200
    if URLMap.query.filter_by(short=short_id).first():
        flash(NOT_UNIQUE_SHORT_ID)
        return render_template('index.html', form=form), 200
    url_map = URLMap(
        original=form.original_link.data,
        short=short_id,
    )
    db.session.add(url_map)
    db.session.commit()
    return render_template(
        'index.html',
        form=form,
        short_url=url_map.get_short_url()), 200


@app.route('/<string:short_id>', methods=['GET'])
def redirect_view(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original), 302