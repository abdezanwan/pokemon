from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.validators import DataRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    pokemon_name = StringField(label='Pokemon Name', validators=[DataRequired()])  
    submit = SubmitField('Login')

class SearchPokemonForm(FlaskForm):
    pokemon_name = StringField(label='Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Search')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')