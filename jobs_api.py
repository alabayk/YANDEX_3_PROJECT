import flask
from flask import jsonify, make_response, request

from data.db_session import create_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = create_session()
    all_jobs = session.query(Jobs).all()
    return jsonify({'jobs': [item.to_dict() for item in all_jobs]})


@blueprint.route('/api/jobs/<int:job_id>')
def get_job_by_id(job_id):
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    return jsonify({'job': job.to_dict()})


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    session = create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'collaborators', 'is_finished', 'job', 'team_leader', 'work_size']):
        return jsonify({'error': 'Bad request'})
    elif request.json['id'] in [j.id for j in session.query(Jobs).all()]:
        return jsonify({'error': 'id already exists'})
    else:
        job = Jobs(id=request.json['id'],
                   job=request.json['job'],
                   collaborators=request.json['collaborators'],
                   team_leader=request.json['team_leader'],
                   work_size=request.json['work_size'],
                   is_finished=request.json['is_finished'])
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session = create_session()
    if job_id not in [j.id for j in session.query(Jobs).all()]:
        return jsonify({'error': 'invalid id'})
    else:
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def put_job(job_id):
    session = create_session()
    if job_id not in [j.id for j in session.query(Jobs).all()]:
        return jsonify({'error': 'invalid id'})
    elif any(key in request.json for key in ['is_finished', 'job', 'team_leader', 'work_size']):
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        if request.json.get('job', 0):
            job.job = request.json['job']
        if request.json.get('is_finished', 0):
            job.is_finished = request.json['is_finished']
        if request.json.get('team_leader', 0):
            job.team_leader = request.json['team_leader']
        if request.json.get('work_size', 0):
            job.work_size = request.json['work_size']
        session.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'invalid data'})


@blueprint.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)
