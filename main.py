from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired

from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


def get_all_jobs(session):
    jobs = session.query(Jobs).all()
    return jobs


def get_user_from_id(session, id):
    user = session.query(User).filter(User.id == id).first()
    return user


def get_teamleaders_for_jobs(session, jobs):
    teamleaders = [get_user_from_id(session, job.team_leader) for job in jobs]
    return teamleaders


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    param = {}
    jobs = get_all_jobs(session)
    teamleaders = get_teamleaders_for_jobs(session, jobs)
    param['jobs_list'] = jobs
    param['team_leaders'] = teamleaders
    return render_template('index.html', **param)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)


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


def add_job(team_leader, job_desctription, work_size, collaborators, is_finished,
            start_date=datetime.datetime.now()):
    session = db_session.create_session()
    job = Jobs()
    job.team_leader = team_leader
    job.job = job_desctription
    job.work_size = work_size
    job.collaborators = collaborators
    job.start_date = start_date
    job.is_finished = is_finished
    session.add(job)
    session.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
