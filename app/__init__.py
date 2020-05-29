from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = 'iamAsecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/covid19'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)

    with app.app_context():
        from . import routes 
        db.create_all()

        return app