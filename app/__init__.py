from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager

from dotenv import load_dotenv
load_dotenv()

from .authentication.routes import auth





app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view='auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth)


from . import routes

from . import models

from . import services




