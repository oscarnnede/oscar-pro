import os
import sys
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# --- Database Connection ---
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_USER', 'admin')
MONGO_PASS = os.getenv('MONGO_PASS', 'pass')
MONGO_DB = os.getenv('MONGO_DB', 'barber_shop')

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

# Print connection details for debugging (remove in production)
print(f"DEBUG: Connecting to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
print(f"DEBUG: Database: {MONGO_DB}")
print(f"DEBUG: URI: mongodb://{MONGO_USER}:****@{MONGO_HOST}:{MONGO_PORT}/")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Force a connection to test it
    client.admin.command('ping')
    db = client[MONGO_DB]
    collection = db['bookings']
    print(f"✅ Connected to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
    print("Continuing without database...")
    collection = None
    db = None

# --- Routes ---
@app.route('/')
def index():
    print("Root route accessed") # Debug log
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    if collection is None:
        return "Database connection failed!", 500
    
    name = request.form.get('name')
    phone = request.form.get('phone')
    service = request.form.get('service')
    time = request.form.get('time')
    
    if not all([name, phone, service, time]):
        return "Missing fields!", 400
    
    booking = {
        'name': name,
        'phone': phone,
        'service': service,
        'time': time,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    result = collection.insert_one(booking)
    
    return f"""
    <h2>Booking Confirmed, {name}!</h2>
    <p>Service: {service} at {time}</p>
    <p>We'll call you at {phone} to confirm.</p>
    <p><small>Booking ID: {result.inserted_id}</small></p>
    <a href="/">Back to Home</a>
    """

@app.route('/bookings')
def view_bookings():
    if collection is None:
        return {"error": "Database connection failed"}, 500
    bookings = list(collection.find({}, {'_id': 0}))
    return jsonify(bookings)

# Add a simple health check
@app.route('/health')
def health():
    return {"status": "ok", "mongodb": collection is not None}

if __name__ == '__main__':
    print("Starting Flask app on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)