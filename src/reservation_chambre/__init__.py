from flask import Flask
from flask_migrate import Migrate
from .database import db 
from .models import Client, Chambre, Reservation

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@<domaine|ip>:<port>/<database>'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/reservation_des_chambres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mysecretkey'

    db.init_app(app)

    migrate.init_app(app, db)

    return app


