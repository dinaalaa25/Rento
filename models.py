import json
import os
import re

class User:
    def __init__(self, first_name, last_name, email, password, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.users_file = os.path.join(os.path.dirname(__file__), 'users.json')

    def validate(self):
        """Validates user data"""
        if not all([self.first_name, self.last_name, self.email, self.password]):
            return False, "All fields are required."
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.email):
            return False, "Invalid email format."
        
        if (len(self.password) < 8 or 
            not re.search(r"[A-Za-z]", self.password) or 
            not re.search(r"[0-9]", self.password) or 
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password)):
            return False, "Weak password."
        
        return True, "Valid user data"

    def save(self):
        """Saves user to JSON file"""
        try:
            # Load existing users   
            users = []
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users = json.load(f)
            
            # Check if email already exists
            if any(user['email'] == self.email for user in users):
                return False, "Email already registered"
            
            # Generate new user ID if not provided
            if not self.id:
                self.id = max([user.get('id', 0) for user in users], default=0) + 1
            
            # Add new user
            users.append({
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password
            })
            
            # Save updated users list
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=4)
            
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error saving user: {str(e)}"

    def authenticate(self):
        """Authenticates user credentials"""
        try:
            if not os.path.exists(self.users_file):
                return False, "User database not found"
            
            with open(self.users_file, 'r') as f:
                users = json.load(f)
                for user in users:
                    if user['email'] == self.email and user['password'] == self.password:
                        return True, {k: user[k] for k in ['first_name', 'last_name', 'email', 'id']}
            
            return False, "Invalid email or password"
        except Exception as e:
            return False, f"Error authenticating user: {str(e)}"


class Car:
    def __init__(self, brand, model, price_per_day, image_url, user_id, car_id=None):
        self.id = car_id
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
        self.image_url = image_url
        self.user_id = user_id
        self.cars_file = os.path.join(os.path.dirname(__file__), 'cars.json')

    def validate(self):
        """Validates car data"""
        if not self.brand or not self.model:
            return False, "Brand and model are required"
        
        try:
            price = float(self.price_per_day)
            if price <= 0:
                return False, "Price must be greater than 0"
        except (ValueError, TypeError):
            return False, "Price must be a valid number"
        
        return True, "Car data is valid"

    @classmethod
    def load_all(cls, user_id=None):
        """Load all cars from JSON file"""
        cars_file = os.path.join(os.path.dirname(__file__), 'cars.json')
        try:
            if os.path.exists(cars_file):
                with open(cars_file, 'r') as f:
                    cars = json.load(f)
                    cars = [car for car in cars if car.get('user_id') == user_id]
                    return cars
            return []
        except Exception as e:
            print(f"Error loading cars: {str(e)}")
            return []

    @classmethod
    def load_by_id(cls, car_id):
        """Load a specific car by ID"""
        cars = cls.load_all()
        return next((car for car in cars if car.get('id') == car_id), None)

    def save(self):
        """Saves car to JSON file"""
        try:
            # Load existing cars
            cars = []
            if os.path.exists(self.cars_file):
                with open(self.cars_file, 'r') as f:
                    cars = json.load(f)
            
            # Generate new ID if not provided
            if not self.id:
                self.id = max([car.get('id', 0) for car in cars], default=0) + 1
            
            # Create car data
            car_data = {
                'id': self.id,
                'brand': self.brand,
                'model': self.model,
                'price_per_day': self.price_per_day,
                'image_url': self.image_url,
                'user_id': self.user_id
            }
            
            # Update existing car or add new one
            car_index = next((i for i, car in enumerate(cars) if car.get('id') == self.id), None)
            if car_index is not None:
                cars[car_index] = car_data
            else:
                cars.append(car_data)
            
            # Save updated cars list
            with open(self.cars_file, 'w') as f:
                json.dump(cars, f, indent=4)
            
            return True, "Car saved successfully"
        except Exception as e:
            return False, f"Error saving car: {str(e)}"

    def delete(self):
        """Deletes car from JSON file"""
        try:
            if not os.path.exists(self.cars_file):
                return False, "Cars database not found"
            
            with open(self.cars_file, 'r') as f:
                cars = json.load(f)
            
            # Remove car with matching ID
            cars = [car for car in cars if car.get('id') != self.id]
            
            with open(self.cars_file, 'w') as f:
                json.dump(cars, f, indent=4)
            
            return True, "Car deleted successfully"
        except Exception as e:
            return False, f"Error deleting car: {str(e)}" 
        
    def rent(self):
        cars = self.load_all()
        car = None
        for car_item in cars:
            if car_item.get('id') == self.id:
                car = car_item
                break
        if car is None:
            return False, "Car not found"
        
        car['user_id'] = self.user_id
        self.save()
        return True, "Car rented successfully"
       