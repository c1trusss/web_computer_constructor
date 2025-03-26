import json
import pprint

from flask import Flask, render_template, request

from config import COMPONENTS
from data import db_session
from data.components import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1trus_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():

    db_session.global_init('db/components.db')
    db_sess = db_session.create_session()

    with open("params.json", 'r', encoding='utf8') as f:
        params_data = json.load(f)

    params = {
        "page_title": "Главная страница",
        "username": "C1truS",
        "params": params_data,
        "type": "Процессор"
    }

    if request.method == 'POST':
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

    details = db_sess.query(search_table).all()
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
    params["attrs"] = {}

    for attr in search_table.columns:
        variants = set(map(lambda x: getattr(x, attr.name), details))
        params["attrs"][attr.name] = sorted(variants)

    return render_template('index.html', **params)


def main():
    db_session.global_init("db/components.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
