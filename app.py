from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.environ.get("MONGO_URI")   # ✅ FIXED
print("Mongo URI:", mongo_uri)

client = MongoClient(mongo_uri)

# Check connection
try:
    client.server_info()
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)

db = client["eventDB"]
collection = db["registrations"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "event": request.form['event']
    }

    result = collection.insert_one(data)
    print("Inserted ID:", result.inserted_id)

    return "Registered Successfully!"
@app.route('/force')
def force():
    print("FORCE ROUTE HIT")   # 👈 must print
    result = collection.insert_one({"test": "working"})
    print("FORCE INSERTED:", result.inserted_id)
    return "Inserted!"


if __name__ == '__main__':
    app.run(debug=True)