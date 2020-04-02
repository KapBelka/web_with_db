import flask
import datetime
from flask import jsonify, request
from werkzeug.exceptions import abort

from data import db_session
from data.users import User
from main import login_manager
from flask_login import login_required

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


def get_one_user(session, user_id):
    user = session.query(User).get(user_id)
    return user


def get_all_users(session):
    users = session.query(User).all()
    return users


@blueprint.route('/api/users')
@login_required
def get_users():
    session = db_session.create_session()
    users = {"users": [user.to_dict() for user in get_all_users(session)]}
    return jsonify(users)


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    session = db_session.create_session()
    user = get_one_user(session, user_id)
    if user:
        user_dict = {"users": [user.to_dict()]}
        return jsonify(user_dict)
    else:
        abort(404)


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in 
                 ['id', 'surname', 'name', 'age', 'position',
                 'city_from', 'speciality', 'address', 'email',
                 'password', 'modified_date']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    password = request.json['password']
    request.json.pop('password')
    request.json['modified_date'] = datetime.datetime.strptime(request.json['modified_date'],
                                                               "%Y-%m-%d-%H.%M.%S")
    user = User(**request.json)
    user.set_password(password)
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/edit/<int:user_id>', methods=['PUT'])
def edit_job(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in 
                 ['id', 'surname', 'name', 'age', 'position',
                 'city_from', 'speciality', 'address', 'email',
                 'password', 'modified_date']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    if 'id' in request.json:
        if request.json['id'] != user_id and session.query(User).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        user.id = request.json['id']
    if 'password' in request.json:
        user.set_password(request.json['password'])
    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'city_from' in request.json:
        user.city_from = request.json['city_from']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'modified_date' in request.json:
        user.modified_date = datetime.datetime.strptime(request.json['modified_date'],
                                                        "%Y-%m-%d-%H.%M.%S")
    session.commit()
    return jsonify({'success': 'OK'})