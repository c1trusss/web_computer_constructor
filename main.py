import json
import os
import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    redirect
)
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import components_resourses
from data import db_session
from data.components import *
from data.users import User
from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1trus_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/auth')
def authorization():
    return render_template('authorization.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Email уже используется!")
        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль!",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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


@app.route('/account')
def account():

    if current_user.is_authenticated:
        user_id = current_user.id

        params = {}

        # ToDo: Строение json: data[user_id][configuration_name] = configuration
        # ToDo: Взять по user_id конфигурации, их названия засунуть в ComboBox
        with open("configurations.json", 'r', encoding='utf8') as file:
            data = json.load(file)
            user_configurations = data[user_id]
            params["user_configs"] = user_configurations
        # ToDo: Под ComboBox разместить поле с выводом текущей конфигурации (скорее всего через циклы в шаблонах)
        # ToDo: Добавить импорт конфигурации в .txt файл

    return render_template("account.html")


def main():
    db_session.global_init("db/components.db")
    api.add_resource(components_resourses.ComponentResource, '/api/<component_class>/<component_id>')
    api.add_resource(components_resourses.ComponentListResource, '/api/<component_class>')

    port = int(os.environ.get("PORT", 8080))
    app.run(port=port)


if __name__ == '__main__':
    main()
