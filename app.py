# Imports needed.
from flask import Flask, request, redirect, url_for, flash
import re, os, json

app = Flask("app")
#-------------------- Utility Functions--------------
# Function that reads and returns the contents of an HTML file from the "templates" folder.
def get_html(page_name):
    with open("templates/" + page_name + ".html", encoding="utf-8") as html_file:
        return html_file.read()


# Path to your JSON file storing user data
users_db = 'users.json'


# Saves user data into a JSON file (appends new entries to the list)
def write_to_json(first_name, last_name, email, password, filename='users.json'):
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    users.append({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    })
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)


# Appends user data into a plain text file (creates the file if it doesn't exist)
def write_to_text(first_name, last_name, email, password, filename='users.txt'):
    try:
        with open(filename, 'a') as file:  # 'a' means append mode (creates file if not exists)
            file.write(f"First Name: {first_name}\n")
            file.write(f"Last Name: {last_name}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Password: {password}\n")
            file.write("-" * 40 + "\n")  # Separator between users
        print("User data written to text file successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# ---------------- FLASK Routes --------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get form data
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Basic validation checks
        if not all([first_name, last_name, email, password, confirm_password]):
            return "All fields are required", 400
        if password != confirm_password:
            return "Passwords do not match", 400

        # Save the user data to both JSON and text files
        write_to_json(first_name, last_name, email, password)
        write_to_text(first_name, last_name, email, password)

        return f"Welcome {first_name} {last_name}!"

    # If GET request, return the signup form HTML
    return get_html('signup')



# Home route - loads the index page and replaces username placeholder
@app.route('/')
def home():
    username = request.cookies.get('username')
    content = get_html('index')
    if username:
        content = content.replace("{{ username }}", username)
    else:
        content = content.replace("{{ username }}", "Guest")
    return content


# Running the app.
if __name__ == '__main__':
    app.run(debug=True)



