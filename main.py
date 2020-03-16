from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()
