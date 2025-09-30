from datetime import datetime, timezone
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from models import SurveySubmission, StoredSurveyRecord
from storage import append_json_line

app = Flask(__name__)
CORS(app, resources={r"/v1/*": {"origins": "*"}})


def generate_submission_id(email: str) -> str:
    """Generate a SHA-256 hash using email + YYYYMMDDHH."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    return hashlib.sha256(f"{email}{timestamp}".encode("utf-8")).hexdigest()


@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })


@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "detail": "Body must be application/json"}), 400

    # Capture user agent if missing
    if "user_agent" not in payload or payload["user_agent"] is None:
        payload["user_agent"] = request.headers.get("User-Agent", "")

    try:
        # Validate raw submission
        submission = SurveySubmission(**payload)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": ve.errors()}), 422

    # Generate submission_id if missing
    if not submission.submission_id:
        submission.submission_id = generate_submission_id(submission.email)

    # Create StoredSurveyRecord with raw values
    record = StoredSurveyRecord(
        **submission.dict(),
        received_at=datetime.now(timezone.utc),
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or "")
    )

    # Hash PII and include received_at and ip before saving
    record_to_save = record.hashed_record()
    record_to_save["received_at"] = record.received_at
    record_to_save["ip"] = record.ip

    append_json_line(record_to_save)

    return jsonify({"status": "ok", "submission_id": submission.submission_id}), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)






