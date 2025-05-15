# This file handles all route definitions for the application.

from flask import Blueprint, request, jsonify, render_template
import re, json, os
from utils import write_to_json, write_to_text, users_db  # Import helpers from utils
from car import Car  # Import our Car class

# Create a blueprint for grouping the routes
main = Blueprint('main','app')

# Route for the homepage
@main.route('/')
def home():
    cars_file = os.path.join(os.path.dirname(__file__), 'cars.json')
    try:
        with open(cars_file, 'r') as f:
            cars_data = json.load(f)
            cars = [Car(**car) for car in cars_data]  # Convert JSON data to Car objects
    except Exception as e:
        cars = []
    return render_template('index.html', cars=cars)

# GET: Render the sign-in page
@main.route('/signin', methods=['GET'])
def signin_page():
    return render_template('signin.html')

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
    return render_template('signup.html')

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

# GET: Render add car page
@main.route('/cars', methods=['GET'])
def add_car_page():
    return render_template('car_details.html', mode='add', car=None)

# POST: Handle add car form submission
@main.route('/cars', methods=['POST'])
def add_car_submit():
    # Extract form data
    body = request.get_json()
    
    # Load cars
    cars_file = os.path.join(os.path.dirname(__file__), 'cars.json')
    try:
        with open(cars_file, 'r') as f:
            cars_data = json.load(f)
    except Exception as e:
        cars_data = []
    
    # Generate new id
    new_id = max([car.get('id', 0) for car in cars_data], default=0) + 1
    
    # Create new car using Car class
    new_car = Car(
        id=new_id,
        model=body.get('model'),
        brand=body.get('brand'),
        price_per_day=int(body.get('price_per_day')),
        image_url=body.get('image_url')
    )
    
    # Convert car object to dict and append to cars list
    cars_data.append(new_car.__dict__)
    
    # Save to file
    with open(cars_file, 'w') as f:
        json.dump(cars_data, f, indent=2)
    
    return jsonify({"message": "Car added successfully!"}), 200

# GET and POST: Edit car
@main.route('/cars/<int:car_id>', methods=['GET', 'POST'])
def car_detail_page(car_id):
    cars_file = os.path.join(os.path.dirname(__file__), 'cars.json')
    try:
        with open(cars_file, 'r') as f:
            cars_data = json.load(f)
    except Exception as e:
        cars_data = []
    
    car_data = next((car for car in cars_data if car.get('id') == car_id), None)
    
    if request.method == 'POST':
        body = request.get_json()
        # Create updated car using Car class
        updated_car = Car(
            id=car_id,
            model=body.get('model'),
            brand=body.get('brand'),
            price_per_day=int(body.get('price_per_day')),
            image_url=body.get('image_url')
        )
        
        # Update car in the list
        for i, car in enumerate(cars_data):
            if car.get('id') == car_id:
                cars_data[i] = updated_car.__dict__
                break
        
        # Save to file
        with open(cars_file, 'w') as f:
            json.dump(cars_data, f, indent=2)
        
        return jsonify({"message": "Car updated successfully!"}), 200
    
    return render_template('car_details.html', mode='edit', car=car_data)