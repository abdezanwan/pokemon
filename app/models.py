from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

# Define your models here


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    ability_name_1 = db.Column(db.String(100))
    ability_name_2 = db.Column(db.String(100))
    image_url = db.Column(db.String(200))
    attack = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    defense = db.Column(db.Integer)

    def __init__(self, name, ability_name_1, ability_name_2, image_url, attack, hp, defense):
        self.name = name
        self.ability_name_1 = ability_name_1
        self.ability_name_2 = ability_name_2
        self.image_url = image_url
        self.attack = attack
        self.hp = hp
        self.defense = defense

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    pokemons = db.relationship('UserPokemon', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class UserPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False, unique=True)  # Make it unique

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
