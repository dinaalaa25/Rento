# This is the entry point of the application. It creates the Flask app and runs it.

from flask import Flask
from routes import main as main_blueprint  # Import the blueprint from routes.py
import os

# Drive the car of your dreams
app = Flask("app")  # Initialize the Flask app

# Configure session
app.secret_key = os.urandom(24)  # Generate a random secret key for session security

# Register the routes (blueprint)
app.register_blueprint(main_blueprint)

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
