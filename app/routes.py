from app import app, db
from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm, SignUpForm, SearchPokemonForm
from .models import User, Pokemon, UserPokemon
from flask_login import current_user, login_user, logout_user, login_required
from flask_bcrypt import check_password_hash  # Import the check_password_hash function
import requests
from app.forms import RegistrationForm, LoginForm, PokemonForm
from flask import render_template
from .forms import SearchPokemonForm


@app.route("/search_pokemon", methods=["GET", "POST"])
@login_required
def search_pokemon():
    form = SearchPokemonForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Handle Pokémon search and database storage logic here

      return render_template('search_pokemon.html', form=form)
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/some_route")
def some_route():
    if current_user.is_authenticated:
        # User is logged in, you can access their information
        username = current_user.username
        # Perform actions for authenticated users

        return render_template('authenticated_template.html', username=username)
    else:
        # User is not logged in, you can handle this case
        return render_template('not_authenticated_template.html')
# @app.route("/fetch_pokemon", methods=["GET", "POST"])
# @login_required
# def fetch_pokemon():
#     form = SearchPokemonForm()

#     try:
#         if request.method == 'POST' and form.validate_on_submit():
#             # Handle Pokémon search and database storage logic here
#             pokemon_name = form.pokemon_name.data

#             # Use the PokeAPI to fetch Pokémon data
#             pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
#             response = requests.get(pokeapi_url)

#             if response.status_code == 200:
#                 data = response.json()
#                 # Extract relevant information from the PokeAPI response
#                 name = data['species']['name']
#                 ability_name_1 = data['abilities'][0]['ability']['name']
#                 ability_name_2 = data['abilities'][1]['ability']['name'] if len(data['abilities']) > 1 else None
#                 image_url = data['sprites']['front_default']
#                 attack = data['stats'][1]['base_stat']
#                 hp = data['stats'][0]['base_stat']
#                 defense = data['stats'][2]['base_stat']

#                 # Create a new Pokémon object and save it to the database
#                 pokemon = Pokemon(name=name, ability_name_1=ability_name_1, ability_name_2=ability_name_2,
#                                   image_url=image_url, attack=attack, hp=hp, defense=defense)

#                 db.session.add(pokemon)
#                 db.session.commit()

#                 flash(f'Fetched and stored data for Pokémon: {pokemon_name}', 'info')
#             else:
#                 flash(f'Failed to fetch data for Pokémon: {pokemon_name}', 'danger')

#     except Exception as e:
#         # Handle exceptions and log them for debugging
#         print(f"Exception occurred: {str(e)}")
#         flash('An error occurred while processing the request', 'danger')

#     return render_template('display_pokemon.html', form=form)

@app.route("/fetch_pokemon", methods=["GET", "POST"])
@login_required
def fetch_pokemon():
    form = SearchPokemonForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Handle Pokémon search and database storage logic here
        pokemon_name = form.pokemon_name.data

        # Use the PokeAPI to fetch Pokémon data
        pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(pokeapi_url)

        if response.status_code == 200:
            data = response.json()
            # Extract relevant information from the PokeAPI response
            name = data['species']['name']
            ability_name_1 = data['abilities'][0]['ability']['name']
            ability_name_2 = data['abilities'][1]['ability']['name'] if len(data['abilities']) > 1 else None
            image_url = data['sprites']['front_default']
            attack = data['stats'][1]['base_stat']
            hp = data['stats'][0]['base_stat']
            defense = data['stats'][2]['base_stat']

            # Create a new Pokémon object and save it to the database
            pokemon = Pokemon(name=name, ability_name_1=ability_name_1, ability_name_2=ability_name_2,
                              image_url=image_url, attack=attack, hp=hp, defense=defense)

            db.session.add(pokemon)
            db.session.commit()

            flash(f'Fetched and stored data for Pokémon: {pokemon_name}', 'info')
        else:
            flash(f'Failed to fetch data for Pokémon: {pokemon_name}', 'danger')

    return render_template('display_pokemon.html', form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    search_form = SearchPokemonForm()
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):  # Check the password hash
                    login_user(user)
                    if 'next' in request.args:
                        return redirect(request.args['next'])
                    else:
                        return redirect(url_for('display_pokemon', name=username))
                else:
                    flash('Invalid username or password', 'danger')
            else:
                flash('User not found', 'danger')

    return render_template('login.html', form=form, search_form=search_form)



@app.route("/display_pokemon/<name>")
@login_required
def display_pokemon(name):
    user = User.query.get(current_user.id)
    return render_template('display_pokemon.html', user=user)