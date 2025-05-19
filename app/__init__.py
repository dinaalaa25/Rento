from flask import Flask
from app.controllers.auth_controller import auth
from app.controllers.car_controller import car
import os

def create_app():
    app = Flask(__name__, 
                static_folder='../static',  # Set the static folder path
                static_url_path='/static')  # Set the URL path for static files
    app.secret_key = 'bakaboza'  
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(car)
    
    return app 