from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another one')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists. Please choose another one')

    username = StringField(label='Username:', validators=[Length(min=3, max=32), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), Length(max=32), DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password_1'), DataRequired()])
    submit = SubmitField(label='Register Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')
