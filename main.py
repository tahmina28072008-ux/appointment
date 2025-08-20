import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Handles Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app) # Enables CORS for all routes

@app.route('/bookAppointment', methods=['POST'])
def book_appointment():
    """
    Handles POST requests to book an appointment.
    This function acts as the webhook for the `bookAppointment` tool.
    """
    # Log the incoming request to the console for debugging
    print(f"Received request with headers: {request.headers}")
    print(f"Received request body: {request.json}")

    # Check if the request has JSON data
    if not request.json:
        return jsonify({"success": False, "message": "Missing JSON data in request."}), 400

    # Extract required parameters from the request body
    symptoms = request.json.get('symptoms')
    doctor_type = request.json.get('doctorType')

    # Basic input validation as specified in the OpenAPI schema
    if not symptoms or not doctor_type:
        return jsonify({
            "success": False,
            "message": "Missing required parameters.",
            "errorMessage": "Symptoms and doctorType are required."
        }), 400

    try:
        # --- Start of simulated business logic ---
        # In a real-world scenario, you would connect to a database,
        # an external API, or another service here to book the appointment.

        # Generate a unique confirmation number
        confirmation_number = os.urandom(4).hex().upper()
        
        # Determine a simulated booking time based on doctor type
        if doctor_type == "General Practitioner":
            booked_time = "Tomorrow, 10:00 AM"
        elif doctor_type == "Dermatologist":
            booked_time = "In 2 days, 2:30 PM"
        else:
            booked_time = "In 5 days, 11:00 AM"
        
        # --- End of simulated business logic ---
        
        # Prepare the successful response
        response = {
            "success": True,
            "message": f"Appointment for {symptoms} with a {doctor_type} has been successfully booked for {booked_time}.",
            "data": {
                "confirmationNumber": confirmation_number,
                "bookedSymptoms": symptoms,
                "bookedDoctorType": doctor_type,
                "bookedTime": booked_time
            }
        }
        
        return jsonify(response), 200

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred. Please try again.",
            "errorMessage": str(e)
        }), 500

if __name__ == '__main__':
    # Cloud Run provides the PORT environment variable.
    # We use 8080 for local testing if the PORT variable isn't set.
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
