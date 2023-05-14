from website import app
from flask import render_template, redirect, url_for, flash
from website.models import Game, User, Key
from website.forms import RegisterForm, LoginForm, AddGame, UpdatePrice, AddKey, DelistGame, AddBalance, PurchaseGame, SupportForm
from website import db
from flask_login import login_user, logout_user, current_user
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

tokenizer1 = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')
model1 = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')


def LoggedIn():
    if current_user.is_authenticated:
        return True
    else:
        return False


def Admin():
    if LoggedIn():
        if current_user.admin:
            return True
        else:
            return False
    else:
        return False


@app.route('/')
@app.route('/home/')

def home_page():
    return render_template('home.html')


@app.route('/register/', methods=['GET', 'POST'])

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
            flash(error[0], category='danger')
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])

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



@app.route('/logout/')
def logout_page():
    logout_user()
    flash('Successfully logged out', category='info')
    return redirect(url_for('home_page'))



@app.route('/admin/')
def admin_page():
    if not Admin():
        return redirect(url_for('home_page'))
    return render_template('admin.html')


@app.route('/admin/add_games/', methods=['GET', 'POST'])
def add_games_page():
    if not Admin():
        return redirect(url_for('home_page'))

    form = AddGame()
    if form.validate_on_submit():
        game = Game(name=form.name.data,
                    price=form.price.data,
                    description=form.description.data,
                    image=form.image.data)
        db.session.add(game)
        db.session.commit()
        flash('Game Added Successfully', category='success')
        return redirect(url_for('add_games_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], category='danger')

    return render_template('add_games.html', form=form)


@app.route('/admin/delist_games/', methods=['GET', 'POST'])
def delist_games_page():
    if not Admin():
        return redirect(url_for('home_page'))

    form = DelistGame()
    if form.validate_on_submit():
        game = Game.query.filter_by(id=form.id.data).first()
        if game:
            if game.available:
                game.available = 0
                Key.query.filter_by(game_id=form.id.data, bought=0).delete()
                db.session.commit()
                flash('Game Delisted Successfully', category='success')
                return redirect(url_for('delist_games_page'))
            else:
                flash('Game Has Already Been Delisted', category='danger')
                return redirect(url_for('delist_games_page'))

        else:
            flash('Game ID Does Not Exist', category='danger')
            return redirect(url_for('delist_games_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], category='danger')

    return render_template('delist_games.html', form=form)


@app.route('/admin/update_price/', methods=['GET', 'POST'])
def update_price_page():
    if not Admin():
        return redirect(url_for('home_page'))
    form = UpdatePrice()
    if form.validate_on_submit():
        game = Game.query.filter_by(id=form.id.data).first()
        if game:
            game.price = form.new_price.data
            db.session.commit()
            flash('Price Updated Successfully', category='success')
            return redirect(url_for('update_price_page'))

        else:
            flash('Game ID Does Not Exist', category='danger')
            return redirect(url_for('update_price_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], category='danger')
    return render_template('update_price.html', form=form)


@app.route('/admin/add_key/', methods=['GET', 'POST'])
def add_key_page():
    if not Admin():
        return redirect(url_for('home_page'))

    form = AddKey()
    if form.validate_on_submit():
        game = Game.query.filter_by(id=form.id.data).first()
        if game:
            new_key = Key(game_id=form.id.data,
                          platform=form.platform.data,
                          value=form.value.data)
            db.session.add(new_key)
            db.session.commit()
            flash('Key Added Successfully', category='success')
            return redirect(url_for('add_key_page'))
        else:
            flash('Game ID Does Not Exist', category='danger')
            return redirect(url_for('add_key_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], category='danger')

    return render_template('add_key.html', form=form)

@app.route('/games/')
def all_games():
    games = Game.query.all()
    return render_template('all_games.html', games=games)

@app.route('/games/<game_id>/<name>', methods=['GET', 'POST'])
def game_page(game_id, name):
    game = Game.query.filter_by(id=game_id).first()
    if game:
        form = PurchaseGame()
        if form.validate_on_submit():
            if not LoggedIn():
                flash('You need an account to purchase a game', category='danger')
                return redirect(url_for('home_page'))
            user = User.query.filter_by(id=current_user.id).first()
            if user.balance < game.price:
                flash('Not Enough Balance To Purchase Game', category='danger')
                return redirect(url_for('home_page'))
            user.balance -= game.price
            db.session.commit()
            flash('Game Purchased Successfully. Key Has Been Sent To Your Email', category='success')
            return redirect(url_for('home_page'))

        if form.errors != {}:
            for error in form.errors.values():
                flash(error[0], category='danger')

        return render_template('game_page.html', game=game, form=form)
    else:
        flash('That Game Does Not Exist', category='danger')
        return redirect(url_for('all_games'))

@app.route('/add_balance/', methods=['GET', 'POST'])
def add_balance():
    if not LoggedIn() or Admin():
        return redirect(url_for('home_page'))

    form = AddBalance()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.balance += form.amount.data
        db.session.commit()
        flash('Balance Updated Successfully', category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], category='danger')

    return render_template('add_balance.html', form=form)
    
@app.route('/support/', methods=['GET', 'POST'])
def support_page():
    form = SupportForm()
    response = None
    if form.validate_on_submit():
        query = form.query.data
        # Generate your response here. This could be a call to a chatbot API, a lookup in a FAQ database, etc.

        text = open("data.txt", "r")
        inputs = tokenizer1(query, text.read(), return_tensors="pt")
        with torch.no_grad():
            outputs = model1(**inputs)

        answer_start_index = torch.argmax(outputs.start_logits)
        answer_end_index = torch.argmax(outputs.end_logits)

        predict_answer_tokens = inputs.input_ids[0, answer_start_index:answer_end_index + 1]
        answer = tokenizer1.decode(predict_answer_tokens)
        
        #response = "This is a placeholder response to the query: " + query
        response = answer

    return render_template('support.html', form=form, response=response)
