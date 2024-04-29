from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('password_again', message='not match')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='not match')])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Имя пользователя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    speciality = StringField('Профессия', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')