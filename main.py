from flask import Flask, render_template, request, make_response, jsonify
from flask_login import login_manager, login_user, logout_user, login_required, LoginManager, \
    current_user
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import *
from wtforms.fields.html5 import *
from wtforms.validators import DataRequired
from requests import get

import users_resourse
import jobs_resourse
import jobs_api, users_api
from data import db_session
from data.categories import Category
from data.departments import Departments
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
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


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class JobAddForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    categories = StringField('Categories', validators=[DataRequired()])
    is_job_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')


class DepartmentAddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    members = StringField('members', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CategoryAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
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


def get_categories_for_jobs(session, jobs):
    categories = []
    for job in jobs:
        temp = []
        for category in job.categories:
            temp.append(str(category.id))
        categories.append(', '.join(temp))
    return categories


def get_all_deparments(session):
    departments = session.query(Departments).all()
    return departments


def get_chiefs_for_departments(session, departments):
    chiefs = [get_user_from_id(session, department.chief) for department in departments]
    return chiefs


def get_all_categories(session):
    categories = session.query(Category).all()
    return categories


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    param = {}
    jobs = get_all_jobs(session)
    teamleaders = get_teamleaders_for_jobs(session, jobs)
    categories = get_categories_for_jobs(session, jobs)
    print(get('http://127.0.0.1:5000/api/users'))
    param['jobs_list'] = jobs
    param['team_leaders'] = teamleaders
    param['categories'] = categories
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job_add',  methods=['GET', 'POST'])
@login_required
def job_add():
    form = JobAddForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            team_leader=current_user.id,
            job=form.job_title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_job_finished.data
        )
        for category_id in form.categories.data.split(', '):
            category = session.query(Category).filter(Category.id == category_id).first()
            if category:
                job.categories.append(category)
        session.add(job)
        session.commit()
        return redirect('/index')
    return render_template('job_add.html', title='Добавление работы', form=form)


@app.route('/job_edit/<int:id>',  methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = JobAddForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                         (current_user.id == 1))).first()
        if job:
            form.job_title.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_job_finished.data = job.is_finished
            form.categories.data = ', '.join([str(category.id) for category in job.categories])
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                         (current_user.id == 1))).first()
        if job:
            job.job = form.job_title.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_job_finished.data
            temp = form.categories.data.split(', ')
            for category_id in temp:
                category = session.query(Category).filter(Category.id == category_id).first()
                if category and category not in job.categories:
                    job.categories.append(category)
            for category in list(job.categories):
                if str(category.id) not in temp:
                    job.categories.remove(category)
            session.commit()
            return redirect('/index')
        else:
            abort(404)
    return render_template('job_add.html', title='Добавление работы', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                     (current_user.id == 1))).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    param = {}
    deparments = get_all_deparments(session)
    chiefs = get_chiefs_for_departments(session, deparments)
    param['departments_list'] = deparments
    param['chiefs'] = chiefs
    return render_template('departments.html', **param)


@app.route('/department_add',  methods=['GET', 'POST'])
@login_required
def department_add():
    form = DepartmentAddForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Departments(
            chief=current_user.id,
            title=form.title.data,
            members=form.members.data,
            email=form.email.data
        )
        session.add(department)
        session.commit()
        return redirect('/departments')
    return render_template('department_add.html', title='Добавление департамента', form=form)


@app.route('/department_edit/<int:id>',  methods=['GET', 'POST'])
@login_required
def department_edit(id):
    form = DepartmentAddForm()
    if request.method == "GET":
        session = db_session.create_session()
        department = session.query(Departments).filter(Departments.id == id,
                                                       ((Departments.chief == current_user.id) |
                                                        (current_user.id == 1))).first()
        if department:
            form.email.data = department.email
            form.members.data = department.members
            form.title.data = department.title
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        department = session.query(Departments).filter(Departments.id == id,
                                                       ((Departments.chief == current_user.id) |
                                                        (current_user.id == 1))).first()
        if department:
            department.email = form.email.data
            department.members = form.members.data
            department.title = form.title.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department_add.html', title='Добавление работы', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    session = db_session.create_session()
    department = session.query(Departments).filter(Departments.id == id,
                                                   ((Departments.chief == current_user.id) |
                                                    (current_user.id == 1))).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/categories')
def categories():
    session = db_session.create_session()
    param = {}
    categories = get_all_categories(session)
    param['categories'] = categories
    return render_template('categories.html', **param)


@app.route('/category_add',  methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryAddForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        category = Category(
            name=form.name.data
        )
        session.add(category)
        session.commit()
        return redirect('/categories')
    return render_template('category_add.html', title='Добавление категории', form=form)


@app.route('/category_edit/<int:id>',  methods=['GET', 'POST'])
@login_required
def category_edit(id):
    form = CategoryAddForm()
    if request.method == "GET":
        session = db_session.create_session()
        category = session.query(Category).filter(Category.id == id, current_user.id == 1).first()
        if category:
            form.name.data = category.name
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        category = session.query(Category).filter(Category.id == id, current_user.id == 1).first()
        if category:
            category.name = form.name.data
            session.commit()
            return redirect('/categories')
        else:
            abort(404)
    return render_template('category_add.html', title='Добавление работы', form=form)


@app.route('/category_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def category_delete(id):
    session = db_session.create_session()
    category = session.query(Category).filter(Category.id == id, current_user.id == 1).first()
    if category:
        session.delete(category)
        session.commit()
    else:
        abort(404)
    return redirect('/categories')


def get_map_part_from_city(city_name):
    geocode_api_server = "http://geocode-maps.yandex.ru/1.x/"
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
    params = {
        "apikey": api_key,
        "geocode": city_name,
        "format": "json"
    }
    response = get(geocode_api_server, params=params)
    if not response:
        abort(404)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    toponym_coordinates = toponym["Point"]["pos"]
    coords = toponym_coordinates.split(' ')
    map_params = {
        "l": "sat",
        "spn": "0.05,0.05",
        "ll": ','.join(coords)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = get(map_api_server, params=map_params)
    if not response:
        abort(404)
    map_file = "map.png"
    with open(f"static/img/{map_file}", "wb") as file:
        file.write(response.content)
    return map_file


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    response = get(f"http://127.0.0.1:5000/api/v2/users/{user_id}")
    if not response:
        abort(404)
    json_response = response.json()
    user = json_response['users'][0]
    city_from = user['city_from']
    map_file = get_map_part_from_city(city_from)
    param = {
        'city_from': city_from,
        'name': user['name'],
        'surname': user['surname'],
        'map_file': map_file
    }
    return render_template('users_show.html', title='Hometown', **param)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(users_resourse.UsersResource, '/api/v2/users/<int:user_id>') 
    api.add_resource(users_resourse.UsersListResource, '/api/v2/users') 
    api.add_resource(jobs_resourse.JobsResource, '/api/v2/jobs/<int:user_id>') 
    api.add_resource(jobs_resourse.JobsListResource, '/api/v2/jobs') 
    app.run()


if __name__ == '__main__':
    main()
