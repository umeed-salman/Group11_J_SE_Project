from website import app
from flask import render_template, redirect, url_for, flash
from website.models import Game, User
from website.forms import RegisterForm
from website.forms import LoginForm
from website import db
from flask_login import login_user, logout_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password_1.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful', category='success')
        return redirect(url_for('login_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error, category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match. Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Successfully logged out', category='info')
    return redirect(url_for('home_page'))
