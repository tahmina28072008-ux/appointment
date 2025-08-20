# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# Create a Flask web server instance
app = Flask(__name__)

# Apply CORS to the app to allow cross-origin requests
CORS(app)

# A simple in-memory list to act as a database for appointments
# In a real-world application, you would use a proper database (e.g., Firestore, MySQL, etc.)
appointments = []

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    """
    Handles a POST request to book a new appointment.
    """
    # Check if the request body is valid JSON
    if not request.json:
        return jsonify({"error": "Invalid request body"}), 400

    # Extract appointment data from the request body
    data = request.json
    patient_name = data.get("patient_name")
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")
    contact_number = data.get("contact_number")
    reason_for_visit = data.get("reason_for_visit")

    # Perform basic validation on the incoming data
    if not all([patient_name, appointment_date, appointment_time, contact_number, reason_for_visit]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new appointment dictionary
    new_appointment = {
        "patient_name": patient_name,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "contact_number": contact_number,
        "reason_for_visit": reason_for_visit
    }

    # Add the new appointment to our in-memory list
    appointments.append(new_appointment)

    # Return a success response
    return jsonify({
        "message": "Appointment booked successfully!",
        "appointment": new_appointment
    }), 201

# Run the application
if __name__ == '__main__':
    # Use the PORT environment variable provided by Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
