from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from api import login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
db = SQLAlchemy(engine_options={"pool_pre_ping": True, "pool_recycle":300})

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def asdict(self):
        return jsonify(id=self.id, username=self.username, email=self.email, password=self.password)
