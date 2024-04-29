from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('ID лидера', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = StringField('Email департамента', validators=[DataRequired()])
    submit = SubmitField('Добавить')