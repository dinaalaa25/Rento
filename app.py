# Imports needed.
from flask import Flask, request, redirect, url_for, flash, jsonify, render_template, session
import re, os, json

app = Flask("app")
app.secret_key = os.urandom(24)  # Secret key for session management

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
@app.route('/signin', methods=['GET'])
def signin_page():
    return get_html('signin')

@app.route('/signin', methods=['POST'])
def signin():
    body = {}
    if request.is_json:
        body = request.get_json()
    else:
        body = request.form

    email = body.get("email")
    password = body.get("password")

    # Basic validation checks
    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    # Validate email format using regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({"message": "Invalid email format."}), 400

    # Validate password strength
    # Password must be at least 8 characters long, contain at least one letter, one number, and one special character
    if (
        len(password) < 8
        or not re.search(r"[A-Za-z]", password)
        or not re.search(r"[0-9]", password)
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        return jsonify({
            "message": (
                "Password must be at least 8 characters long, contain at least one letter, "
                "one number, and one special character."
            )
        }), 400

    # Check if user exists in JSON file
    try:
        with open(users_db, 'r') as file:
            users = json.load(file)
            for user in users:
                if user["email"] == email and user["password"] == password:
                    session["user"] = {
                        "first_name": user["first_name"],
                        "last_name": user["last_name"],
                        "email": user["email"]
                    }
                    return redirect(url_for('home'))
            return jsonify({"message": "Invalid email or password."}), 401
    except FileNotFoundError:
        return jsonify({"message": "User database not found."}), 500
    except json.JSONDecodeError:
        return jsonify({"message": "Error reading user database."}), 500

@app.route('/signup', methods=['GET'])
def signup_page():
    return get_html('signup')

@app.route('/signup', methods=['POST'])
def signup():
    body = {}
    if request.is_json:
        body = request.get_json()
    else:
        body = request.form

    new_user = {
        "first_name": body.get("first_name"),
        "last_name": body.get("last_name"),
        "email": body.get("email"),
        "password": body.get("password")
    }

    # Basic validation checks
    for field, value in new_user.items():
        if not value:
            return jsonify({"message": f"{field.replace('_', ' ').title()} is required."}), 400

    # Validate email format using regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_user['email']):
        return jsonify({"message": "Invalid email format."}), 400


    # Validate password strength
    # Password must be at least 8 characters long, contain at least one letter, one number, and one special character
    if (
        len(new_user["password"]) < 8
        or not re.search(r"[A-Za-z]", new_user["password"])
        or not re.search(r"[0-9]", new_user["password"])
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_user["password"])
    ):
        return jsonify({
            "message": (
                "Password must be at least 8 characters long, contain at least one letter, "
                "one number, and one special character."
            )
        }), 400

    # Save the user data to both JSON and text files
    write_to_json(new_user["first_name"], new_user["last_name"], new_user["email"], new_user["password"])
    write_to_text(new_user["first_name"], new_user["last_name"], new_user["email"], new_user["password"])

    response_user = {
        "first_name": new_user["first_name"],
        "last_name": new_user["last_name"],
        "email": new_user["email"]
    }
    session["user"] = response_user

    return redirect(url_for('home'))

#-------

# Home route - loads the index page and replaces username placeholder
@app.route('/')
def home():
    user = session.get('user')
    content = get_html('index')
    if user and 'first_name' in user:
        content = content.replace('<span id="username_display"></span>',
        f'<span id="usernameDisplay">{user["first_name"]}</span>')
    else:
        return redirect(url_for('signin_page'))
    return content


# Running the app.
if __name__ == '__main__':
    app.run(debug=True)



