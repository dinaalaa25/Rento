import os

def get_html(page_name):
    try:
        with open(f'templates/{page_name}.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {page_name}.html not found"

def get_heading():
    try:
        with open('static/text/heading.txt', 'r') as f:
            return f"<h1>{f.readline().strip()}</h1>"
    except:
        return "<h1>Explore Our Cars</h1>"

def custom_hash(text):
    result = []
    # Loop through each character and its position
    for i, char in enumerate(text, 1):
        # Get ASCII code and multiply by position
        ascii_code = ord(char)
        hashed_value = ascii_code * i
        result.append(str(hashed_value))
    
    # Join all numbers with dashes
    return '-'.join(result)
    