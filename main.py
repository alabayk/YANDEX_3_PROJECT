from datetime import datetime

from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

import jobs_api
import jobs_resource
import users_api
import users_resource
from data import db_session
from data.departments import Department
from data.forms.add_dep_form import AddDepartmentForm
from data.forms.add_work_form import AddWorkForm
from data.forms.login_form import LoginForm
from data.forms.register_form import RegisterForm
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


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


def main():
    db_session.global_init(r"C:\Yandex\Flask-YaL\db\jobs.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route("/jobs_list")
def jobs_list():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    us = {}
    for u in users:
        us.update({u.id: u.surname + ' ' + u.name})
    return render_template("jobs_list.html", jobs=jobs, us=us)


@app.route("/add_job", methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddWorkForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        users_ids = [u.id for u in session.query(User).all()]
        if form.team_leader.data not in users_ids:
            form.team_leader.errors = 'Нет пользователя с таким ID!'
            return render_template('add_job.html', form=form, title='Добавление работы', error='1')
        else:

            new_job = Jobs(job=form.job.data,
                           work_size=form.work_size.data,
                           collaborators=form.collaborators.data,
                           is_finished=form.is_finished.data,
                           team_leader=form.team_leader.data)
            session.add(new_job)
            session.commit()
            return redirect('/jobs_list')
    return render_template('add_job.html', form=form, title='Добавление работы')


@app.route("/corr_job/<job_id>", methods=['GET', 'POST'])
@login_required
def corr_job(job_id):
    form = AddWorkForm()
    session = db_session.create_session()
    if (current_user.id == session.query(Jobs).filter(Jobs.id == job_id).first().team_leader) or (current_user.id == 1):
        if form.validate_on_submit():
            correct_job = session.query(Jobs).filter(Jobs.id == job_id).first()
            correct_job.job = form.job.data
            correct_job.work_size = form.work_size.data
            correct_job.collaborators = form.collaborators.data
            correct_job.is_finished = form.is_finished.data
            correct_job.team_leader = form.team_leader.data
            session.commit()
            return redirect('/jobs_list')
        return render_template('add_job.html', title='Редактирование работы', form=form,
                               job=session.query(Jobs).filter(Jobs.id == job_id).first())
    else:
        return 'Ошибка доступа!'


@app.route("/del_job/<job_id>", methods=['GET', 'POST'])
@login_required
def del_job(job_id):
    session = db_session.create_session()
    if (current_user.id == session.query(Jobs).filter(Jobs.id == job_id).first().team_leader) or (current_user.id == 1):
        to_del_job = session.query(Jobs).filter(Jobs.id == job_id).first()
        session.delete(to_del_job)
        session.commit()
        return redirect('/jobs_list')
    else:
        return 'Ошибка доступа!'


@app.route("/departments_list")
def departments_list():
    session = db_session.create_session()
    departments = session.query(Department).all()
    users = session.query(User).all()
    us = {}
    for u in users:
        us.update({u.id: u.surname + ' ' + u.name})
    return render_template("departments_list.html", departments=departments, us=us)


@app.route("/add_dep", methods=['GET', 'POST'])
@login_required
def add_dep():
    form = AddDepartmentForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        new_dep = Department(title=form.title.data,
                             chief=form.chief.data,
                             members=form.members.data,
                             email=form.email.data)
        session.add(new_dep)
        session.commit()
        return redirect('/departments_list')
    return render_template('add_dep.html', form=form, title='Добавление работы')


@app.route("/corr_dep/<dep_id>", methods=['GET', 'POST'])
@login_required
def corr_dep(dep_id):
    form = AddDepartmentForm()
    session = db_session.create_session()
    if (current_user.id == session.query(Department).filter(Department.id == dep_id).first().chief) or (
            current_user.id == 1):
        if form.validate_on_submit():
            to_corr_dep = session.query(Department).filter(Department.id == dep_id).first()
            to_corr_dep.title = form.title.data
            to_corr_dep.chief = form.chief.data
            to_corr_dep.email = form.email.data
            session.commit()
            return redirect('/departments_list')
        return render_template('add_dep.html', title='Редактирование департамента', form=form,
                               dep=session.query(Department).filter(Department.id == dep_id).first())
    else:
        return 'Ошибка доступа!'


@app.route("/del_dep/<dep_id>", methods=['GET', 'POST'])
@login_required
def del_dep(dep_id):
    session = db_session.create_session()
    if (current_user.id == session.query(Department).filter(Department.id == dep_id).first().chief) or (
            current_user.id == 1):
        session.delete(session.query(Department).filter(Department.id == dep_id).first())
        session.commit()
        return redirect('/departments_list')
    else:
        return 'Ошибка доступа!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    age=int(form.age.data),
                    position=form.position.data,
                    speciality=form.speciality.data,
                    address=form.address.data,
                    email=form.login.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.login.data).first()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/okay')
def okay():
    return 'Вы успешно зарегистрированы в системе!'


if __name__ == '__main__':
    main()
