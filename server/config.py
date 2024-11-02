import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# This can be set using environment variables or directly here
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

class Config:
    UPLOAD_FOLDER = os.path.join(PARENT_DIR, 'image_uploads')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PARENT_DIR, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress a warning

db = SQLAlchemy()