# Rento - Car Rental Website  
**Rento** is a user-friendly web application that allows individuals to list, browse, rent, and manage cars easily. It provides a clean interface to manage car rental operations, making it easy for users to find available cars or manage their own listings.

---

### ✅ What does it do?  
This is a web project that allows users to register, log in, add their own cars for rent, browse other available cars, and rent or unrent them. Users can also update or delete their car listings.

---

### 🆕 What is the "new feature" which you have implemented that we haven't seen before?  
- Reading from and writing to a JSON file
- Reading from a text file
- User can add, update, and delete their cars  
- Sending values to routes and handling them using Flask  
- Filtering cars based on ownership and rental status  
- Using **JavaScript with localStorage** to retain user info or interactions  
- Displaying dynamic HTML content with JavaScript

---

## 🔧 Prerequisites  
Before running this project, ensure you have the following installed:

- **Python:** Version 3.12.7 or later  
- **Flask:** Install Flask using pip  
  ```bash
  pip install Flask
  ```  
- **VS Code:** Recommended editor with Python extension enabled

### ▶️ Run Instructions:  
1. Open your terminal in the project directory  
2. Set Flask environment and run the app:  
   ```bash
   $env:FLASK_APP = "run.py"      # On Windows PowerShell  
   flask run
   ```

---

## ✅ Project Checklist  

- [x] It is available on GitHub  
- [x] It uses the Flask web framework  
- [x] It uses at least one module from the Python Standard Library other than `random`  
  - **Modules used:** `json`, `os`, `re`  
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.
  - **File name for the class definition:** `car.py`
  - **Line number(s) for the class definition:** Line 5
  - **Name of two properties:**
    - `brand`
    - `price_per_day`
  - **Name of two methods:**
    - `validate`
    - `save`
  - **File name and line numbers where the methods are used:**
    - `car_controller.py`:
      - `validate`: Line 86, Line 125 
      - `save`: Line 91, Line 130
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser  
- [x] It uses modern JavaScript (`let`, `const`, arrow functions)  
- [x] It makes use of the reading and writing to the same JSON file  
- [x] It contains conditional statements  
  - **File name:** `auth_controller.py`  
  - **Line number(s):** 18, 28, 53, 62
  - **File name:** `car_controller.py`
  - **Lie number(s):** 11, 18, 23, 57, 59, 68, 87, 162, 209...
- [x] It contains loops  
  - **File name(s):** `car_controller.py`  
  - **Line number(s):** 18, 27, 178, 184
- [x] It lets the user enter a value in a text box at some point (add/update car, sign in/up).This value is received and processed by your back end
Python code.  
- [x] It doesn't generate any error message even if the user
enters a wrong input.  
- [x] It is styled using my own CSS  
- [x] The code follows the code and style conventions as
introduced in the course, is fully documented using comments
and doesn't contain unused or experimental code.
In particular, the code should not use `print()` or
`console.log()` for any information the app user should see.
Instead, all user feedback needs to be visible in the
browser.  
- [x] All exercises have been completed as per the
requirements and pushed to the respective GitHub repository.
