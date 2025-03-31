import json
import os
import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
    send_from_directory
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

    with open("metadata.json", 'r', encoding='utf8') as file:
        metadata = json.load(file)
        if current_user.is_authenticated:
            user_metadata = metadata.get(str(current_user.id), {})
        else:
            user_metadata = {}
    selected_value = "Процессор"

    params = {
        "page_title": "Главная страница",
        "params": params_data,
        "type": user_metadata.get("type", selected_value),
        "message": ""
    }

    if request.method == 'POST':

        if 'submit' in request.form:
            # Получение типа комплектующего из ComboBox
            selected_value = request.form.get('chooseType')
            params["type"] = selected_value
            user_metadata["type"] = selected_value

    search_table = None
    match user_metadata.get("type", "Процессор"):
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

    if selected_value and current_user.is_authenticated:
        user_metadata["type"] = selected_value
        metadata[str(current_user.id)] = user_metadata
        with open("metadata.json", "w", encoding='utf8') as outfile:
            json.dump(metadata, outfile, ensure_ascii=False, indent=4)

    all_details = session.query(search_table).all()

    params["attrs"] = {}

    for attr in search_table.columns:
        variants = set(map(lambda x: getattr(x, attr.name), all_details))
        params["attrs"][attr.name] = sorted(variants)

    query = None
    if request.method == 'POST' and request.form.get("submit"):
        # Получение активных чекбоксов
        active_checkboxes_dict = {}
        for attr in params['attrs']:
            active_checkboxes = request.form.getlist(attr)
            if active_checkboxes:
                active_checkboxes_dict[attr] = active_checkboxes
        query = []
        for attr in active_checkboxes_dict:
            column = getattr(search_table, attr)
            query.append(column.in_(active_checkboxes_dict[attr]))
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

    if request.method == 'POST':
        if 'add-btn' in request.form:
            detail = json.loads(request.form.get("add-btn"))
            with open("configurations.json", "r", encoding="utf8") as f:
                data = json.load(f)

                configurations = data.get(str(current_user.id), {
                    "current_cfg": {}
                })
                current_configuration = configurations["current_cfg"]

                current_configuration[detail["component_type"]] = {
                    "cost": detail["cost"],
                    "title": detail["title"]
                }

                configurations["current_cfg"] = current_configuration

                data[str(current_user.id)] = configurations

            with open("configurations.json", "w", encoding='utf8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)

        elif 'save-btn' in request.form:
            cfg_name = request.form.get('cfg_name')
            if not cfg_name:
                params["message"] = "Введите название конфигурации!"
            else:
                with open("configurations.json", "r", encoding='utf8') as f:
                    data = json.load(f)
                    configurations = data.get(str(current_user.id), {})
                    current_config = configurations["current_cfg"]
                    configurations[cfg_name] = current_config
                    data[str(current_user.id)] = configurations

                with open("configurations.json", "w", encoding='utf8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)

        session.close()

    return render_template('index.html', **params)


@app.route('/account', methods=['GET', 'POST'])
def account():

    with open("metadata.json", 'r', encoding='utf8') as file:
        metadata = json.load(file)
        user_metadata = metadata.get(str(current_user.id), {})

    params = {}

    if request.method == 'POST':
        user_metadata["cfg_name"] = request.form.get("chooseConfig")

    params["user_metadata"] = user_metadata
    metadata[str(current_user.id)] = user_metadata

    with open("metadata.json", "w", encoding='utf8') as outfile:
        json.dump(metadata, outfile, ensure_ascii=False, indent=4)

    if current_user.is_authenticated:
        user_id = str(current_user.id)

        with open("configurations.json", 'r', encoding='utf8') as cfgs_file:
            cfgs_data = json.load(cfgs_file)
            params["configs"] = cfgs_data[user_id]
            params["cfg_name"] = user_metadata["cfg_name"]
            print(cfgs_data[user_id])

        for config_name in cfgs_data[user_id]:
            if config_name != 'current_cfg':
                filename = f"{user_id}_{config_name}"
                print(config_name)
                print(filename)
                config = cfgs_data[user_id][config_name]

                with open(f"files/{filename}.txt", "w", encoding='utf8') as file:
                    text = '\n'.join([f"{component}: {config[component]["title"]} - {config[component]["cost"]}р."
                                      for component in config])
                    text += f"\n\nИтого: {sum([int(config[component]["cost"]) for component in config])}"
                    file.write(text)

    return render_template("account.html", **params)


@app.route('/files/<int:user_id>/<string:filename>')
def download_file(user_id, filename):
    # Безопасная отдача файла из папки /files
    return send_from_directory(
        directory='files',
        path=f"{user_id}_{filename}",
        as_attachment=True  # Заставляет браузер скачивать файл
    )


def main():
    db_session.global_init("db/components.db")
    api.add_resource(components_resourses.ComponentResource, '/api/<component_class>/<component_id>')
    api.add_resource(components_resourses.ComponentListResource, '/api/<component_class>')

    port = int(os.environ.get("PORT", 8080))
    app.run(port=port)


if __name__ == '__main__':
    main()
