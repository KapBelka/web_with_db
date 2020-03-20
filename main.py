from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['username'] = "Ученик Яндекс.Лицея"
    param['title'] = 'Приветствие'
    return render_template('index.html', **param)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
