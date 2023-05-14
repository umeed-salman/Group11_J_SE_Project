from website import db, login_manager
from website import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    price = db.Column(db.Numeric(3, 2), nullable=False)
    description = db.Column(db.String(length=1000), nullable=False)
    available = db.Column(db.Integer(), nullable=False, default=1)
    image = db.Column(db.String(length=200), nullable=False, unique=True)
    transactions = db.relationship('Transaction', backref='game', lazy=True)
    keys = db.relationship('Key', backref='game', lazy=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    admin = db.Column(db.Integer(), nullable=False, default=0)
    username = db.Column(db.String(length=32), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    balance = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Key(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    game_id = db.Column(db.Integer(), db.ForeignKey('game.id'), nullable=False)
    value = db.Column(db.String(length=12), nullable=False, unique=True)
    platform = db.Column(db.String(), nullable=False)
    bought = db.Column(db.Integer(), nullable=False, default=0)
    transaction = db.relationship('Transaction', backref='key', uselist=False)


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer(), db.ForeignKey('game.id'), nullable=False)
    key_id = db.Column(db.Integer(), db.ForeignKey('key.id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
