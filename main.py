import json

from flask import Flask, render_template, request

from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1trus_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():

    with open("params.json", 'r', encoding='utf8') as f:
        params_data = json.load(f)

    params = {
        "title": "Главная страница",
        "username": "C1truS",
        "params": params_data,
        "type": "Процессор"
    }

    if request.method == 'POST':
        selected_value = request.form.get('chooseType')
        params["type"] = selected_value

    return render_template('index.html', **params)


def main():
    db_session.global_init("db/components.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
