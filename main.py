from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import redirect
from wtforms import PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired
import datetime

from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def base(title):
    param = {}
    param['title'] = title
    return render_template('base.html', **param)


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param['prof'] = prof
    return render_template('training.html', **param)


@app.route('/list_prof/<list>')
def list_prof(list):
    profs = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию', 'климатолог']
    param = {}
    param['profs'] = profs
    param['list_type'] = list
    return render_template('list_prof.html', **param)


@app.route('/auto_answer')
@app.route('/answer')
def auto_answer():
    param = {}
    param['title'] = "Анкета"
    param['surname'] = "Watny"
    param['name'] = "Mark"
    param['education'] = "выше среднего"
    param['profession'] = "штурман марсохода"
    param['sex'] = "male"
    param['motivation'] = "Всегда мечтал застрять на Марсе!"
    param['ready'] = True
    return render_template('auto_answer.html', **param)


class LoginForm(FlaskForm):
    astronaut_id = IntegerField('Id астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    capitan_id = IntegerField('Id капитана', validators=[DataRequired()])
    capitan_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class ImageForm(FlaskForm):
    file = FileField('Добавить картинку', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Отправить')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/distribution')
def distribution():
    param = {}
    param['astronaut_list'] = ["Ридли Скотт", "Энди Уир", "Марк Уотни", "Венката Капур",
                               "Тедди Сандерс", "Шон Бин"]
    return render_template('distribution.html', **param)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    param = {}
    param["sex"] = sex
    param["age"] = age
    return render_template('cabin.html', **param)


img_items = []
with open(f"static/config/img_items.txt", "r") as f:
    for line in f.readlines():
        img_items.append(line)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    form = ImageForm()
    if form.data["file"]:
        file_name = form.data['file'].filename
        today = datetime.datetime.today()
        full_file_name = f"[{today.strftime('%Y-%m-%d-%H.%M.%S')}]{file_name}"
        with open(f"static/img/{full_file_name}", "wb") as f:
            f.write(form.data["file"].read())
        img_items.append(full_file_name)
        with open(f"static/config/img_items.txt", "a") as f:
            f.write(full_file_name + "\n")
    param = {}
    param["img_items"] = img_items
    return render_template('carousel.html', form=form, **param)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()
