# This file contains utility functions used across the app (file writing, HTML loading, etc.)

import json

# Path to the JSON file used for storing users
users_db = 'users.json'

# Load and return the HTML content of a page from the templates folder
def get_html(page_name):
    with open(f"templates/{page_name}.html", encoding="utf-8") as html_file:
        return html_file.read()

# Write user data to a JSON file (create or append)
def write_to_json(first_name, last_name, email, password, filename=users_db):
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []  # Initialize if file doesn't exist

    users.append({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    })

    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)

# Append user data to a plain text file
def write_to_text(first_name, last_name, email, password, filename='users.txt'):
    with open(filename, 'a') as file:
        file.write(f"First Name: {first_name}\n")
        file.write(f"Last Name: {last_name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Password: {password}\n")
        file.write("-" * 40 + "\n")  # Visual separator between users
