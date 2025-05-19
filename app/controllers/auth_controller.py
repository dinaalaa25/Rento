from flask import Blueprint, request, jsonify, redirect, session
from app.models.user import User
from app.utils.helpers import custom_hash, get_html

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET'])
def signin_page():
    return get_html('signin')

@auth.route('/signin', methods=['POST'])
def signin():
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")

    # Basic validation
    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    # Hash the password before authentication
    hashed_password = custom_hash(password)
    
    # Create user object and authenticate with hashed password
    user = User(None, None, email, hashed_password)
    success, result = user.authenticate()
    
    if success:
        # Store user ID in session
        session['user_id'] = result.get('id')
        return jsonify(result), 200
    return jsonify({"message": result}), 401

@auth.route('/signup', methods=['GET'])
def signup_page():
    return get_html('signup')

@auth.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    original_password = body.get("password")

    # Create user object with original password for validation
    user = User(
        first_name=body.get("first_name"),
        last_name=body.get("last_name"),
        email=body.get("email"),
        password=original_password
    )

    # Validate user data
    is_valid, message = user.validate()
    if not is_valid:
        return jsonify({"message": message}), 400

    # Hash the password after validation
    hashed_password = custom_hash(original_password)
    user.password = hashed_password

    # Save user
    success, message = user.save()
    if success:
        user_data = {k: getattr(user, k) for k in ['first_name', 'last_name', 'email', 'id']}
        session['user_id'] = user_data['id']
        return jsonify(user_data), 201
    return jsonify({"message": message}), 400

@auth.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/signin') 