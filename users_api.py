import flask
from flask import jsonify, make_response, request

from data.db_session import create_session
from data.jobs import Jobs
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_jobs():
    session = create_session()
    all_users = session.query(User).all()
    return jsonify({'users': [item.to_dict() for item in all_users]})


@blueprint.route('/api/users/<int:user_id>')
def get_job_by_id(user_id):
    session = create_session()
    user = session.query(User).filter(User.id == user_id).first()
    return jsonify({'job': user.to_dict()})


@blueprint.route('/api/users', methods=['POST'])
def add_job():
    session = create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'speciality', 'address',
                  'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    elif request.json['id'] in [j.id for j in session.query(User).all()]:
        return jsonify({'error': 'id already exists'})
    else:
        user = User(
            id=request.json['id'],
            name=request.json['name'],
            surname=request.json['surname'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email'],
            hashed_password=request.json['hashed_password']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_job(user_id):
    session = create_session()
    if user_id not in [u.id for u in session.query(User).all()]:
        return jsonify({'error': 'invalid id'})
    else:
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_job(user_id):
    session = create_session()
    if user_id not in [u.id for u in session.query(User).all()]:
        return jsonify({'error': 'invalid id'})
    elif any(key in request.json for key in ['name', 'surname', 'age',
                                             'position', 'speciality', 'address',
                                             'email', 'hashed_password']):
        user = session.query(User).filter(User.id == user_id).first()

        if request.json.get('name', 0):
            user.name = request.json['name']
        if request.json.get('surname', 0):
            user.surname = request.json['surname']
        if request.json.get('age', 0):
            user.age = request.json['age']
        if request.json.get('position', 0):
            user.position = request.json['position']
        if request.json.get('speciality', 0):
            user.speciality = request.json['speciality']
        if request.json.get('address', 0):
            user.address = request.json['address']
        if request.json.get('email', 0):
            user.email = request.json['email']
        if request.json.get('hashed_password', 0):
            user.hashed_password = request.json['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'invalid data'})


@blueprint.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Server error'}), 500)
