import json
import os

class Car:
    def __init__(self, brand, model, price_per_day, image_url, user_id, rented_by_id = None, car_id=None):
        self.id = car_id
        self.brand = brand
        self.model = model
        self.price_per_day = price_per_day
        self.image_url = image_url
        self.user_id = user_id
        self.rented_by_id = rented_by_id
        self.cars_file = os.path.join(os.path.dirname(__file__), '../../db/cars.json')

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
    def load_all(cls):
        """Load all cars from JSON file"""
        cars_file = os.path.join(os.path.dirname(__file__), '../../db/cars.json')
        try:
            if os.path.exists(cars_file):
                with open(cars_file, 'r') as f:
                    cars = json.load(f)
                return cars
            return []
        except Exception as e:
            return []

    @classmethod
    def load_by_id(cls, car_id):
        """Load a specific car by ID"""
        cars = cls.load_all()
        for car in cars:
            if car.get('id') == car_id:
                return car
        return None

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
                'user_id': self.user_id,
                'rented_by_id': self.rented_by_id
            }
            
            # Update existing car or add new one
            car_index = None
            for i in range(len(cars)):
                if cars[i].get('id') == self.id:
                    car_index = i
                    break
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
        
        car['rented_by_id'] = self.rented_by_id
        self.save()
        return True, "Car rented successfully"
    
    def unrent(self):
        cars = self.load_all()
        car = None
        for car_item in cars:
            if car_item.get('id') == self.id:
                car = car_item
                break   
        if car is None:
            return False, "Car not found"
        
        car['rented_by_id'] = None
        self.save()
        return True, "Car unrented successfully" 