from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage, URLMapException
from .models import URLMap

NO_REQUEST_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
NO_SHORT = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url():
    if not request.data:
        raise InvalidAPIUsage(NO_REQUEST_DATA)
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    try:
        url_map = URLMap.create(
            original=data['url'],
            short=data.get('custom_id')
        )
    except URLMapException as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsage(NO_SHORT, 404)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
