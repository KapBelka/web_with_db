from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
import datetime
from data import db_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True)


parser_for_put = reqparse.RequestParser()
parser_for_put.add_argument('id')
parser_for_put.add_argument('team_leader')
parser_for_put.add_argument('job')
parser_for_put.add_argument('work_size')
parser_for_put.add_argument('collaborators')
parser_for_put.add_argument('is_finished')


def get_one_job(session, job_id):
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    return job


def get_all_jobs(session):
    jobs = session.query(Jobs).all()
    return jobs


class JobsResource(Resource):
    def get(self, job_id):
        session = db_session.create_session()
        job = get_one_job(session, job_id)
        if job:
            job_dict = {"jobs": [job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators',
                                                'start_date', 'end_date', 'is_finished'))]}
            return jsonify(job_dict)
        else:
            abort(404)

    def delete(self, job_id):
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if not job:
            return jsonify({'error': 'Not found'})
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        args = parser_for_put.parse_args()
        session = db_session.create_session()
        job = get_one_job(session, job_id)
        if not job:
            return jsonify({'error': 'Not found'})
        if args['id']:
            if request.json['id'] != job_id and session.query(Jobs).get(request.json['id']):
                return jsonify({'error': 'Id already exists'})
            job.id = args['id']
        if args['team_leader']:
            job.team_leader = args['team_leader']
        if args['job']:
            job.job = args['job']
        if args['work_size']:
            job.work_size = args['work_size']
        if args['collaborators']:
            job.collaborators = args['collaborators']
        if args['is_finished']:
            job.is_finished = args['is_finished']
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = {"jobs": [job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators',
                                        'start_date', 'end_date', 'is_finished'))
                         for job in get_all_jobs(session)]}
        return jsonify(jobs)

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
            return jsonify({'error': 'Id already exists'})
        job = Jobs(
                id=args['id'],
                team_leader=args['team_leader'],
                job=args['job'],
                work_size=args['work_size'],
                collaborators=args['collaborators'],
                is_finished=args['is_finished']
            )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})