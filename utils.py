# This file contains utility functions used across the app (file writing, HTML loading, etc.)

import json
import os

# Path to the JSON file used for storing users
users_db = os.path.join(os.path.dirname(__file__), 'users.json')

# Write user data to a JSON file (create or append)
def write_to_json(**user_data):
    try:
        with open(users_db, 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    users.append(user_data)
    
    with open(users_db, 'w') as f:
        json.dump(users, f, indent=2)

def get_html(page_name):
    try:
        with open(f'templates/{page_name}.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {page_name}.html not found"

