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


def add_colonist(surname, name, age, position, speciality, address, email, hashed_password):
    session = db_session.create_session()
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.position = position
    user.speciality = speciality
    user.address = address
    user.email = email
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    add_colonist("Scott", "Ridley", 21, "captain", "research engineer", "module_1",
                 "scott_chief@mars.org", "cap")
    add_colonist("Uir", "Endi", 23, "colonist", "builder", "module_1", "endi_col@mars.org", "enuir")
    add_colonist("Uotni", "Mark", 19, "colonist", "main engineer", "module_1", "mark_u@mars.org",
                 "markiu")
    add_colonist("Bin", "Shon", 21, "colonist", "doctor", "module_1", "shon_bin@mars.org",
                 "binbinshon")
    app.run()


if __name__ == '__main__':
    main()
