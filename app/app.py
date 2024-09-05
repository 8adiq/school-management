from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# loading environments variables
load_dotenv()

# creating a sqlalchemy db instance
db = SQLAlchemy()

def create_app():

    # creating a flask app instance
    app = Flask(__name__)

    # connecting to postgres database
    app.config['SQLALCHEMY_DATABASE_URI']  = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # binding the sqlalchemy to the flask app
    db.init_app(app)

    # importing all blueprint routes
    from routes import all_routes
    all_routes(app,db)


    # setting up database migration
    migrate = Migrate(app,db)
    
    return app