from flask import abort, flash, redirect, render_template
from http import HTTPStatus

from . import app
from .error_handlers import URLException
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
        )
    except URLException as error:
        flash(error.message)
        return render_template('index.html', form=form), HTTPStatus.OK
    return render_template(
        'index.html',
        form=form,
        short=url_map.get_short_url()), HTTPStatus.OK


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    short_obj = URLMap.get_short(short)
    if not short_obj:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(short_obj.original), HTTPStatus.FOUND
