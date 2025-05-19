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
        self.users_file = os.path.join(os.path.dirname(__file__), '../../db/users.json')

    def validate(self):
        """Validates user data"""
        if not all([self.first_name, self.last_name, self.email, self.password]):
            return False, "All fields are required."
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.email):
            return False, "Invalid email format."
        
        # Password validation matching client-side rules
        if len(self.password) < 8:
            return False, "Password must be at least 8 characters long."
        
        if not re.search(r"[A-Za-z]", self.password):
            return False, "Password must contain at least one letter."
            
        if not re.search(r"[0-9]", self.password):
            return False, "Password must contain at least one number."
            
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.password):
            return False, "Password must contain at least one special character."
        
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