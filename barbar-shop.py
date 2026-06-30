from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

# --- Database Connection (Reads from Environment Variables) ---
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb') # 'mongodb' is the service name in Docker Compose
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_USER', 'oscarn')
MONGO_PASS = os.getenv('MONGO_PASS', 'wizzy94')
MONGO_DB = os.getenv('MONGO_DB', 'barber_shop')

# Connection string (MongoDB authentication)
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db['bookings'] # Collection (like a table)
    # Create an index on timestamp for efficient sorting
    collection.create_index('timestamp')
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
    # We don't exit here so the container stays up for debugging, but ideally you'd handle this.

# --- Routes ---
@app.route('/')
def index():
    return render_template('barbar-shop.html')

@app.route('/book', methods=['POST'])
def book():
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
    
    # Insert into MongoDB (instead of JSON file)
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
    # Fetch all bookings, exclude MongoDB's internal '_id' for clean JSON
    bookings = list(collection.find({}, {'_id': 0}))
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)