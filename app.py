from flask import Flask, render_template, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mapping of airline codes to airline names
AIRLINE_MAP = {
    "6E": "IndiGo",
    "AI": "Air India",
    "SG": "SpiceJet",
    "UK": "Vistara",
    "G8": "Go First",
    "I5": "AirAsia India"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form data
        flight_number = request.form.get("flight_number", "").strip().upper()
        arrival_date = request.form.get("arrival_date", "").strip()

        if not flight_number or not arrival_date:
            return render_template("index.html", error="⚠️ Please enter both Flight Number and Arrival Date.")

        # Airline name mapping
        airline_code = flight_number[:2]
        airline_name = AIRLINE_MAP.get(airline_code, "Unknown Airline")

        # Convert arrival_date into datetime
        try:
            scheduled_date = datetime.strptime(arrival_date, "%Y-%m-%d")
        except ValueError:
            return render_template("index.html", error="⚠️ Invalid date format.")

        # Simulate scheduled & predicted times
        scheduled_time = scheduled_date.replace(hour=14, minute=30)  # default scheduled 2:30 PM
        delay_minutes = random.choice([-15, 0, 10, 20, 45, 60])     # simulate early, on-time, or delayed
        predicted_time = scheduled_time + timedelta(minutes=delay_minutes)

        # Confidence score (random but realistic)
        confidence_score = f"{random.randint(70, 99)}%"

        # AI reasoning simulation
        reasons = [
            "Weather conditions at the destination airport.",
            "Air traffic congestion on the route.",
            "Technical checks required before departure.",
            "Smooth operations, no expected delay.",
            "Crew scheduling adjustments."
        ]
        reason = random.choice(reasons)

        # Status classification
        if delay_minutes > 30:
            status_text = "Delayed"
            status_class = "text-red-500"
        elif delay_minutes > 0:
            status_text = "Slight Delay"
            status_class = "text-yellow-400"
        elif delay_minutes < 0:
            status_text = "Early Arrival"
            status_class = "text-green-400"
        else:
            status_text = "On Time"
            status_class = "text-green-400"

        prediction = {
            "flight_number": f"{flight_number} ({airline_name})",
            "scheduled_time": scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "predicted_time": predicted_time.strftime("%Y-%m-%d %H:%M"),
            "delay_minutes": delay_minutes,
            "status_text": status_text,
            "status_class": status_class,
            "reason": reason,
            "confidence_score": confidence_score
        }

        return render_template("index.html", prediction=prediction)

    except Exception as e:
        return render_template("index.html", error=f" An error occurred: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
