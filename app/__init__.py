from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login_page'

app = Flask(__name__)  # Create the app object here

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

from . import routes
from .models import User  # Import User inside create_app to avoid circular import

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
