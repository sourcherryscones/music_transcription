from flask import Flask, Blueprint
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
login_manager = LoginManager()
# removed db = SQLAlchemy() and the globals at the top of create_app; wondering if that does anything

def create_app(conf_class=Config):
    print('CREATE APP HAPPENED GUYS')
    from .auth import User, db
    app = Flask(__name__)
    app.config.from_object(conf_class)
    db.init_app(app)
    login_manager.init_app(app)

    #blueprint setup
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from .main import main as main_bp
    app.register_blueprint(main_bp)
    return app