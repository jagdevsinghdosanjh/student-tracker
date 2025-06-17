from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

mongo = PyMongo()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    # Blueprint registration (move these inside the function)
    from app.routes.students import student_bp
    from app.routes.scores import score_bp
    from app.routes.main import main_bp
    from app.routes.dashboard import dashboard_bp  # Add this

    # Then register it:
    app.register_blueprint(dashboard_bp)  # This line tells Flask about your dashboard routes
    app.register_blueprint(main_bp)
    app.register_blueprint(score_bp, url_prefix='/scores')   
    app.register_blueprint(student_bp, url_prefix='/students')   
    return app

# from flask import Flask
# from flask_pymongo import PyMongo
# from dotenv import load_dotenv
# import os
# from app.routes.scores import score_bp
# app.register_blueprint(score_bp, url_prefix='/scores')
# mongo = PyMongo()

# def create_app():
#     load_dotenv()
#     app = Flask(__name__)
#     app.config["MONGO_URI"] = os.getenv("MONGO_URI")
#     mongo.init_app(app)
#     # Blueprint registration
#     from app.routes.students import student_bp
#     app.register_blueprint(student_bp, url_prefix='/students')
#     return app
