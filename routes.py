# This file handles all route definitions for the application.

from flask import Blueprint, request, jsonify, redirect, session
from utils import get_html, get_heading
from models import User, Car

# Create a blueprint for grouping the routes
main = Blueprint('main','app')

# Route for the homepage
@main.route('/')
def home():
    html_page = get_html('index')
    cars = Car.load_all()
    user_id = session.get('user_id')
    cars = [car for car in cars if car.get('user_id') != user_id and car.get('rented_by_id') == None]
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
                    <button class="delete-btn" onclick="rentCar(event, $car_id$)">Rent Now</button>
                </div>
            </div>
        '''
        
        # Replace each placeholder with actual value
        car_card = car_card.replace("$image$", car.get('image_url', '/static/images/default-car.jpg'))
        car_card = car_card.replace("$brand$", car.get('brand', ''))
        car_card = car_card.replace("$model$", car.get('model', ''))
        car_card = car_card.replace("$price$", str(car.get('price_per_day', 0)))
        car_card = car_card.replace("$car_id$", str(car.get('id', 0)))
        
        car_cards += car_card
    
    html_page = html_page.replace("$car_cards$", car_cards)
    html_page = html_page.replace("$user_id$", str(user_id))
    return html_page

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
        # Store user ID in session
        session['user_id'] = result.get('id')
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
        user_data = {k: getattr(user, k) for k in ['first_name', 'last_name', 'email', 'id']}
        session['user_id'] = user_data['id']
        return jsonify(user_data), 201
    return jsonify({"message": message}), 400

# GET: Render add/edit car page
@main.route('/cars', methods=['GET'])
def car_page():
    car_id = request.args.get('id')
    user_id = session.get('user_id')
    
    if car_id:
        car = Car.load_by_id(int(car_id))
        if not car:
            return redirect('/')
    html_page = get_html('car_details')
    html_page = html_page.replace("$user_id$", str(user_id))
    return html_page

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
    user_id = session.get('user_id')
    # Create car object
    car = Car(
        brand=body.get("brand"),
        model=body.get("model"),
        price_per_day=body.get("price_per_day"),
        image_url=body.get("image_url"),
        user_id=user_id
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
    # Get current user's ID from session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "You must be logged in to update a car"}), 401

    # Get the existing car
    existing_car = Car.load_by_id(car_id)
    if not existing_car:
        return jsonify({"message": "Car not found"}), 404

    # Check if the user owns the car
    if existing_car.get('user_id') != user_id:
        return jsonify({"message": "You can only update your own cars"}), 403

    body = request.get_json()
    
    # Create car object with user_id
    car = Car(
        brand=body.get("brand"),
        model=body.get("model"),
        price_per_day=body.get("price_per_day"),
        image_url=body.get("image_url"),
        user_id=user_id,  # Add the user_id
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
    # Get current user's ID from session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "You must be logged in to delete a car"}), 401

    # Get the existing car
    existing_car = Car.load_by_id(car_id)
    if not existing_car:
        return jsonify({"message": "Car not found"}), 404

    # Check if the user owns the car
    if existing_car.get('user_id') != user_id:
        return jsonify({"message": "You can only delete your own cars"}), 403

    # Create car object with the existing car's data
    car = Car(
        brand=existing_car['brand'],
        model=existing_car['model'],
        price_per_day=existing_car['price_per_day'],
        image_url=existing_car['image_url'],
        user_id=user_id,
        car_id=car_id
    )
    
    success, message = car.delete()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# Logout route
@main.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/signin')

# GET: Render my cars page
@main.route('/<int:user_id>/cars', methods=['GET'])
def my_cars_page(user_id):
    html_page = get_html('my_cars')
    user_id = session.get('user_id')

    cars = Car.load_all()
    cars = [car for car in cars if car.get('user_id') == user_id or car.get('rented_by_id') == user_id]
    
    if not cars:
        return html_page.replace("$car_cards$", '<p class="no-cars">You haven\'t added any cars yet. Add your first car!</p>')
    
    car_cards = ""
    for car in cars:    
        # Create car card HTML with direct replacements
        car_card = '''
            <div class="car-card">
                <img src="$image$" alt="$brand$ $model$">
                <h2>$brand$ $model$</h2>
                <span class="$status_class$">$status$</span>
                <p class="car-price"><span>Price:</span> $$price$/Day</p>
                <div class="card-actions">
                    $action_buttons$
                </div>
            </div>
        '''
        
        # Replace each placeholder with actual value
        car_card = car_card.replace("$image$", car.get('image_url', '/static/images/default-car.jpg'))
        car_card = car_card.replace("$brand$", car.get('brand', ''))
        car_card = car_card.replace("$model$", car.get('model', ''))
        car_card = car_card.replace("$price$", str(car.get('price_per_day', 0)))
        car_card = car_card.replace("$id$", str(car.get('id', 0)))
        car_card = car_card.replace("$status$", "Rented" if car.get('rented_by_id') == user_id else "Owner")
        car_card = car_card.replace("$status_class$", "rented" if car.get('rented_by_id') == user_id else "owner")
        
        # Add action buttons only if user is the owner
        action_buttons = ""
        if car.get('user_id') == user_id:
            action_buttons = f'''
                <a href="/cars?id={car.get('id', 0)}" class="edit-btn">Edit</a>
                <button class="delete-btn" onclick="openDeleteModal({car.get('id', 0)}, '{car.get('brand', '')} {car.get('model', '')}')">Delete</button>
            '''
        elif car.get('rented_by_id') == user_id:
            action_buttons = f'''
                <button class="delete-btn" onclick="unrentCar(event, {car.get('id', 0)})">Unrent</button>
            '''
        car_card = car_card.replace("$action_buttons$", action_buttons)
        
        car_cards += car_card
    html_page = html_page.replace("$car_cards$", car_cards)
    html_page = html_page.replace("$user_id$", str(user_id))
    return html_page

@main.route('/cars/<int:car_id>/rent', methods=['POST'])
def rent_car(car_id):
    old_car = Car.load_by_id(car_id)
    user_id = session.get('user_id')
    
    if not old_car:
        return jsonify({"message": "Car not found"}), 404
    car = Car(old_car['brand'], old_car['model'], old_car['price_per_day'], old_car['image_url'], old_car['user_id'], user_id, car_id)
    success, message = car.rent()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# POST: Unrent car
@main.route('/cars/<int:car_id>/unrent', methods=['POST'])
def unrent_car(car_id):
    old_car = Car.load_by_id(car_id)
    user_id = session.get('user_id')
    
    if not old_car:
        return jsonify({"message": "Car not found"}), 404
    if old_car.get('rented_by_id') != user_id:
        return jsonify({"message": "You can only unrent your own cars"}), 403
    car = Car(old_car['brand'], old_car['model'], old_car['price_per_day'], old_car['image_url'], old_car['user_id'], None, car_id)
    success, message = car.unrent()
    if success:
        return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# Catch-all route for undefined routes
@main.route('/<path:path>')
def catch_all(path):
    return redirect('/signin')
