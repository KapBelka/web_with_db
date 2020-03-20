from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime

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
    add_job(1, "deployment of residential modules 1 and 2", 15, "2, 3", False)
    app.run()


if __name__ == '__main__':
    main()
