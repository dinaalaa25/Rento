# This file handles all route definitions for the application.

from flask import Blueprint, request, jsonify, redirect
from utils import get_html, get_heading
from models import User, Car

# Create a blueprint for grouping the routes
main = Blueprint('main','app')

# Route for the homepage
@main.route('/')
def home():
    html_page = get_html('index')
    cars = Car.load_all()
    
    # Get the heading from the text file and replace the placeholder
    heading = get_heading()
    html_page = html_page.replace("$heading$", heading)
    
    if not cars:
        return html_page.replace("$car_cards$", '<p class="no-cars">No cars available. Add your first car!</p>')
    
    car_cards = ""
    for car in cars:
        # Create car card HTML with direct replacements
        car_card = '''
            <div class="car-card">
                <img src="$image$" alt="$brand$ $model$">
                <h2>$brand$ $model$</h2>
                <p class="car-price"><span>Price:</span> $$price$/Day</p>
                <div class="card-actions">
                    <a href="/cars?id=$id$" class="edit-btn">Edit</a>
                    <button class="delete-btn" onclick="openDeleteModal($id$, '$brand$ $model$')">Delete</button>
                </div>
            </div>
        '''
        
        # Replace each placeholder with actual value
        car_card = car_card.replace("$image$", car.get('image_url', '/static/images/default-car.jpg'))
        car_card = car_card.replace("$brand$", car.get('brand', ''))
        car_card = car_card.replace("$model$", car.get('model', ''))
        car_card = car_card.replace("$price$", str(car.get('price_per_day', 0)))
        car_card = car_card.replace("$id$", str(car.get('id', 0)))
        
        car_cards += car_card
    
    return html_page.replace("$car_cards$", car_cards)

# GET: Render the signin page
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

    # Create user object and authenticate
    user = User(None, None, email, password)
    success, result = user.authenticate()
    
    if success:
        return jsonify(result), 200
    return jsonify({"message": result}), 401

# GET: Render the signup page
@main.route('/signup', methods=['GET'])
def signup_page():
    return get_html('signup')

# POST: Handle sign-up form submission
@main.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()

    # Create user object
    user = User(
        first_name=body.get("first_name"),
        last_name=body.get("last_name"),
        email=body.get("email"),
        password=body.get("password")
    )

    # Validate user data
    is_valid, message = user.validate()
    if not is_valid:
        return jsonify({"message": message}), 400

    # Save user
    success, message = user.save()
    if success:
        return jsonify({k: getattr(user, k) for k in ['first_name', 'last_name', 'email']}), 201
    return jsonify({"message": message}), 400

# GET: Render add/edit car page
@main.route('/cars', methods=['GET'])
def car_page():
    car_id = request.args.get('id')
    if car_id:
        car = Car.load_by_id(int(car_id))
        if not car:
            return redirect('/')
    return get_html('car_details')

# GET: Get all cars
@main.route('/cars/list', methods=['GET'])
def get_all_cars():
    cars = Car.load_all()
    return jsonify(cars)

# GET: Get single car
@main.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = Car.load_by_id(car_id)
    if car:
        return jsonify(car)
    return jsonify({"message": "Car not found"}), 404

# POST: Add new car
@main.route('/cars', methods=['POST'])
def add_car():
    body = request.get_json()
    
    # Create car object
    car = Car(
        brand=body.get("brand"),
        model=body.get("model"),
        price_per_day=body.get("price_per_day"),
        image_url=body.get("image_url")
    )
    
    # Validate car data
    is_valid, message = car.validate()
    if not is_valid:
        return jsonify({"message": message}), 400
    
    # Save car
    success, message = car.save()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# PUT: Update car
@main.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    body = request.get_json()
    
    # Create car object
    car = Car(
        brand=body.get("brand"),
        model=body.get("model"),
        price_per_day=body.get("price_per_day"),
        image_url=body.get("image_url"),
        car_id=car_id
    )
    
    # Validate car data
    is_valid, message = car.validate()
    if not is_valid:
        return jsonify({"message": message}), 400
    
    # Save car
    success, message = car.save()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# DELETE: Delete car
@main.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car(None, None, None, None, car_id)
    success, message = car.delete()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# Logout route
@main.route('/logout')
def logout():
    return redirect('/signin')