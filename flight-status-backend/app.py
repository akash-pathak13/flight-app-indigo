from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import requests

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['flightdb']
flights_collection = db['flights']

# Firebase Cloud Messaging setup
FCM_SERVER_KEY = 'YOUR_SERVER_KEY_HERE'  # Replace with your actual server key
FCM_URL = 'https://fcm.googleapis.com/fcm/send'

def send_fcm_notification(token, message_body):
    headers = {
        'Authorization': f'key={FCM_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'to': token,
        'notification': {
            'title': 'Flight Status Update',
            'body': message_body
        }
    }
    response = requests.post(FCM_URL, headers=headers, json=payload)
    return response.json()

@app.route('/flights', methods=['GET'])
def get_flights():
    flights = list(flights_collection.find({}, {'_id': 0}))
    return jsonify(flights)

@app.route('/update-flight-status', methods=['POST'])
def update_flight_status():
    data = request.get_json()
    flight_number = data['flightNumber']
    new_status = data['status']
    
    flights_collection.update_one(
        {'flightNumber': flight_number},
        {'$set': {'status': new_status}}
    )

    # Here I would typically retrieve the tokens of users interested in this flight
    # For simplicity, let's assume a single token for now
    user_token = 'USER_FCM_TOKEN'  # Replace with the actual user's FCM token
    notification_message = f"Flight {flight_number} status has changed to {new_status}."
    send_fcm_notification(user_token, notification_message)
    
    return jsonify({'message': 'Flight status updated and notification sent.'})

if __name__ == '__main__':
    app.run(debug=True)
