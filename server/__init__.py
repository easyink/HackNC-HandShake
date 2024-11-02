from flask import Flask
from server.config import db, jwt, Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # from server.auth.models import User
    # from server.posts.models import Post
    # from server.images.models import Image

    # from server.auth import auth_bp
    # app.register_blueprint(auth_bp)

    # from server.posts import posts_bp
    # app.register_blueprint(posts_bp)

    # from server.images import images_bp
    # app.register_blueprint(images_bp)

    # from server.ai import ai_bp
    # app.register_blueprint(ai_bp)

    # from server.get import get_bp
    # app.register_blueprint(get_bp)

    return app