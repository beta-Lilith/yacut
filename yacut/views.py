from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .error_handlers import URLMapException
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form), HTTPStatus.OK
    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
            validate=False,
        )
    except URLMapException as error:
        flash(error)
        return render_template('index.html', form=form), HTTPStatus.OK
    return render_template(
        'index.html',
        form=form,
        short_url=url_map.get_short_url()), HTTPStatus.OK


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    short = URLMap.get(short)
    if not short:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(short.original), HTTPStatus.FOUND
