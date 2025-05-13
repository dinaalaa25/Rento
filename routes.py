# This file handles all route definitions for the application.

from flask import Blueprint, request, jsonify
import re, json
from utils import get_html, write_to_json, write_to_text, users_db  # Import helpers from utils

# Create a blueprint for grouping the routes
main = Blueprint('main','app')

# Route for the homepage
@main.route('/')
def home():
    return get_html('index')  # Render index.html

# GET: Render the sign-in page
@main.route('/signin', methods=['GET'])
def signin_page():
    return get_html('signin')

# POST: Handle sign-in form submission
@main.route('/signin', methods=['POST'])
def signin():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    # Basic validation
    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    # Validate email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({"message": "Invalid email format."}), 400

    # Validate password strength
    if (
        len(password) < 8
        or not re.search(r"[A-Za-z]", password)
        or not re.search(r"[0-9]", password)
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        return jsonify({"message": "Weak password."}), 400

    # Check if user exists in the JSON file
    try:
        with open(users_db, 'r') as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email and user["password"] == password:
                    return jsonify(user), 200
            return jsonify({"message": "Invalid email or password."}), 401
    except FileNotFoundError:
        return jsonify({"message": "User database not found."}), 500
    except json.JSONDecodeError:
        return jsonify({"message": "Error reading user database."}), 500

# GET: Render the signup page
@main.route('/signup', methods=['GET'])
def signup_page():
    return get_html('signup')

# POST: Handle sign-up form submission
@main.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()

    # Collect user fields
    new_user = {
        "first_name": body.get("first_name"),
        "last_name": body.get("last_name"),
        "email": body.get("email"),
        "password": body.get("password")
    }

    # Ensure no field is missing
    for field, value in new_user.items():
        if not value:
            return jsonify({"message": f"{field.replace('_', ' ').title()} is required."}), 400

    # Email format check
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_user['email']):
        return jsonify({"message": "Invalid email format."}), 400

    # Password strength check
    if (
        len(new_user["password"]) < 8
        or not re.search(r"[A-Za-z]", new_user["password"])
        or not re.search(r"[0-9]", new_user["password"])
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_user["password"])
    ):
        return jsonify({"message": "Weak password."}), 400

    # Save the user to both JSON and text
    write_to_json(**new_user)
    write_to_text(**new_user)

    # Return only safe info
    return jsonify({k: new_user[k] for k in ["first_name", "last_name", "email"]}), 201
