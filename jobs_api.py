import flask
from flask import jsonify, request
from werkzeug.exceptions import abort

from data import db_session
from data.jobs import Jobs
from main import get_all_jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


def get_one_job(session, job_id):
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    return job


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = {"jobs": [job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators',
                                       'start_date', 'end_date', 'is_finished'))
                     for job in get_all_jobs(session)]}
    return jsonify(jobs)


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    session = db_session.create_session()
    job = get_one_job(session, job_id)
    if job:
        job_dict = {"jobs": [job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators',
                                               'start_date', 'end_date', 'is_finished'))]}
        return jsonify(job_dict)
    else:
        abort(404)


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in 
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
            id=request.json['id'],
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished']
        )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/edit/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in 
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    if 'id' in request.json:
        if request.json['id'] != job_id and session.query(Jobs).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        job.id = request.json['id']
    if 'team_leader' in request.json:
        job.team_leader = request.json['team_leader']
    if 'job' in request.json:
        job.job = request.json['job']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})
