import json
import os

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response
)
from flask_restful import Api
from sqlalchemy import or_

import components_resourses
from data import db_session
from data.components import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1trus_secret_key'

api = Api(app)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/', methods=['GET', 'POST'])
def index():

    db_session.global_init('db/components.db')
    session = db_session.create_session()

    with open("params.json", 'r', encoding='utf8') as f:
        params_data = json.load(f)

    params = {
        "page_title": "Главная страница",
        "username": "C1truS",
        "params": params_data,
        "type": "Процессор"
    }

    if request.method == 'POST':

        # Получение типа комплектующего из ComboBox
        selected_value = request.form.get('chooseType')
        params["type"] = selected_value

    search_table = None
    match params["type"]:
        case 'Процессор':
            search_table = CPU
        case 'Видеокарта':
            search_table = GPU
        case 'Корпус':
            search_table = Core
        case 'Материнская плата':
            search_table = Motherboard
        case 'Оперативная память':
            search_table = RAM
        case 'Устройство памяти':
            search_table = Disk
        case 'Блок питания':
            search_table = Power
        case 'Кулер для ЦП':
            search_table = CPUCoolers

    all_details = session.query(search_table).all()

    params["attrs"] = {}
    for attr in search_table.columns:
        variants = set(map(lambda x: getattr(x, attr.name), all_details))
        params["attrs"][attr.name] = sorted(variants)

    query = None
    if request.method == 'POST':
        # Получение активных чекбоксов
        active_checkboxes_dict = {}
        for attr in params['attrs']:
            active_checkboxes = request.form.getlist(attr)
            if active_checkboxes:
                active_checkboxes_dict[attr] = active_checkboxes
        query = [
            eval(
                f"{search_table.__name__}.{attr}.in_({active_checkboxes_dict[attr]})"
            ) for attr in active_checkboxes_dict
        ]
    if query:
        details = session.query(search_table).filter(*query)
    else:
        details = session.query(search_table).all()
    details_list = []
    for detail in details:
        detail_dict = {
            "title": detail.title,
            "cost": detail.cost,
            "image": f"static/img/{detail.image}",
            "link": detail.link
        }
        details_list.append(detail_dict)

    params['details'] = details_list

    return render_template('index.html', **params)


def main():
    db_session.global_init("db/components.db")
    api.add_resource(components_resourses.ComponentResource, '/api/<component_class>/<component_id>')
    api.add_resource(components_resourses.ComponentListResource, '/api/<component_class>')

    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)


if __name__ == '__main__':
    main()
