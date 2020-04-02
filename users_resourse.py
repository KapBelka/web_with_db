from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
import datetime
from data import db_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('city_from', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


parser_for_put = reqparse.RequestParser()
parser_for_put.add_argument('surname')
parser_for_put.add_argument('name')
parser_for_put.add_argument('age', type=int)
parser_for_put.add_argument('position')
parser_for_put.add_argument('city_from')
parser_for_put.add_argument('speciality')
parser_for_put.add_argument('address')
parser_for_put.add_argument('email')
parser_for_put.add_argument('password')


def get_one_user(session, user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user


def get_all_users(session):
    users = session.query(User).all()
    return users


def check_email(session, email):
    user = session.query(User).filter(User.email == email).first()
    if user:
        abort(400, message=f"Email {email} already exist")


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = get_one_user(session, user_id)
        user_dict = {"users": [user.to_dict()]}
        return jsonify(user_dict)

    def delete(self, user_id):
        session = db_session.create_session()
        user = get_one_user(session, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser_for_put.parse_args()
        session = db_session.create_session()
        user = get_one_user(session, user_id)
        if args['password']:
            user.set_password(args['password'])
        if args['surname'] in args:
            user.surname = args['surname']
        if args['name'] in args:
            user.name = args['name']
        if args['age'] in args:
            user.age = args['age']
        if args['position'] in args:
            user.position = args['position']
        if args['city_from'] in args:
            user.city_from = args['city_from']
        if args['speciality'] in args:
            user.speciality = args['speciality']
        if args['address'] in args:
            user.address = args['address']
        if args['email'] in args:
            check_email(session, args['email'])
            user.email = args['email']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = {"users": [user.to_dict() for user in get_all_users(session)]}
        return jsonify(users)

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        check_email(session, args['email'])
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            city_from=args['city_from'],
            speciality=args['speciality'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})