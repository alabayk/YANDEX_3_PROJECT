from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class AddWorkForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Время на выполнение', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')
    team_leader = IntegerField('ID лидера команды', validators=[DataRequired()])
    collaborators = StringField('Выполняющие работу', validators=[DataRequired()])
    submit = SubmitField('Добавить')