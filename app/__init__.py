
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///leaderboard.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "change-this-in-prod")
    # Simple in-memory cache (can be swapped to Redis by changing config)
    app.config["CACHE_TYPE"] = os.environ.get("CACHE_TYPE", "SimpleCache")
    app.config["CACHE_DEFAULT_TIMEOUT"] = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))

    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import routes, auth, swagger  # register routes and blueprints
        db.create_all()

    return app
