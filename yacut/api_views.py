from flask import jsonify, request

from yacut import app, db
from .error_handlers import InvalidAPIUsage
from .models import MAX_SHORT_LENGTH, URLMap
from .utils import get_unique_short_id, valid_short_id


NO_REQUEST_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
NOT_UNIQUE_SHORT_ID = 'Предложенный вариант короткой ссылки уже существует.'
NO_SHORT_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url():
    if not request.data:
        raise InvalidAPIUsage(NO_REQUEST_DATA)
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    short_id = data.get('custom_id')
    if not short_id:
        short_id = get_unique_short_id()
    if len(short_id) > MAX_SHORT_LENGTH:
        raise InvalidAPIUsage(INVALID_SHORT_ID)
    if not valid_short_id(short_id):
        raise InvalidAPIUsage(INVALID_SHORT_ID)
    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(NOT_UNIQUE_SHORT_ID)
    url_map = URLMap()
    url_map.from_dict(dict(original=data['url'], short=short_id))
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    short_id_obj = URLMap.query.filter_by(short=short_id).first()
    if not short_id_obj:
        raise InvalidAPIUsage(NO_SHORT_ID, 404)
    return jsonify({'url': short_id_obj.original}), 200
