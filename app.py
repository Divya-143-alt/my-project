from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# --------------------
# MongoDB setup
# --------------------
mongo_uri = os.environ.get("MONGO_URI")  # Set this in Render
client = MongoClient(mongo_uri)
db = client["eventDB"]              # Database name
collection = db["registrations"]   # Collection name

# --------------------
# Routes
# --------------------
@app.route('/')
def home():
    return render_template('index.html')

# ⚠ Route must allow POST to prevent 405
@app.route('/register', methods=['POST'])
@app.route('/register/',methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    event = request.form.get('event')

    if name and email and event:
        collection.insert_one({"name": name, "email": email, "event": event})
        return "✅ Registered Successfully!"
    else:
        return "⚠ All fields are required.", 400

# Optional test route
@app.route('/force')
def force():
    result = collection.insert_one({"test": "working"})
    return f"Force Inserted: {result.inserted_id}"

# --------------------
# Run server
# --------------------
if __name__ == '__main__':
    app.run(debug=True)