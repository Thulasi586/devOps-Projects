import os
from flask import Flask, jsonify, request
from twilio.rest import Client

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/mock-alert", methods=["POST"])
def mock_alert():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "Demo alert: monitoring service is down.")

    return jsonify({
        "status": "MOCK ALERT",
        "message": message,
        "phone_call_made": False
    }), 200

@app.route("/alert", methods=["POST"])
def alert():
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_PHONE_NUMBER")
    to_number = os.environ.get("ALERT_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        return jsonify({"error": "Twilio environment variables are missing"}), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "Monitoring alert: a service may be down.")

    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            twiml=(
                "<Response><Say>"
                "Monitoring alert. Please check your application."
                "</Say></Response>"
            ),
        )
        return jsonify({"status": "call initiated", "call_sid": call.sid}), 200
    except Exception:
        app.logger.exception("Twilio call failed")
        return jsonify({"error": "Could not initiate the alert call"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
