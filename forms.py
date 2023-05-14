from flask_wtf import FlaskForm
from wtforms import Field, IntegerField, DecimalField, StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
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

    username = StringField(label='Username:', validators=[Length(min=3, max=32, message='Username must be between 3 and 32 characters long'), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), Length(max=32, message='Email must be less than 32 characters'), DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[Length(min=8, message='Password must be at least 8 characters long'), DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password_1', message='Passwords do not match'), DataRequired()])
    submit = SubmitField(label='Register Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class AddGame(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    price = DecimalField(label='Price:', validators=[DataRequired(), NumberRange(min=0, max=150,
                                                                                 message='Price must be between 0 and 150')])
    image = StringField(label='Image URL', validators=[DataRequired()])
    description = TextAreaField(label='Description:', validators=[DataRequired()])
    submit = SubmitField(label='Add Game')


class DelistGame(FlaskForm):
    id = IntegerField(label='ID:', validators=[DataRequired()])
    submit = SubmitField(label='Delist Game')


class UpdatePrice(FlaskForm):
    id = IntegerField(label='ID:', validators=[DataRequired()])
    new_price = DecimalField(label='Price:', validators=[DataRequired(), NumberRange(min=0, max=150,
                                                                                     message='New price must be between 0 and 150')])
    submit = SubmitField(label='Update')


class AddKey(FlaskForm):
    id = IntegerField(label='ID:', validators=[DataRequired()])
    value = StringField(label='Key:', validators=[Length(min=12, max=12, message='Key must be exactly 12 characters long'), DataRequired()])
    platform = SelectField(label='Platform', choices=['PC', 'Xbox One', 'Xbox Series X', 'PS4', 'PS5'])
    submit = SubmitField(label='Add Key')

class AddBalance(FlaskForm):
    amount = IntegerField(label='Amount:', validators=[DataRequired(), NumberRange(min=10, max=200, message='Amount must be between 10 and 200')])
    number = StringField(label='Card Number:', validators=[DataRequired(), Length(min=16, max=16, message='Card number must be exactly 16 digits long')])
    cvv = StringField(label='CVV:', validators=[DataRequired(), Length(min=3, max=3, message='CVV must be exactly 3 digits long')])
    submit = SubmitField(label='Add Balance')

class PurchaseGame(FlaskForm):
    platform = SelectField(label='Platform', choices=['PC', 'Xbox One', 'Xbox Series X', 'PS4', 'PS5'])
    submit = SubmitField(label='Purchase')