from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email
from wtforms.fields.html5 import EmailField

class SignUp(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = EmailField('email', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Wrong Password')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class AddItem(FlaskForm):
    text = TextAreaField('Text', validators =[InputRequired()])
    submit = SubmitField('Add')