# Survey Intake API

A lightweight backend service I built and further developed for collecting and storing post-interaction survey responses. The API validates incoming data, handles deduplication, and saves submissions in an append-only NDJSON format. This project was a experiment in backend development, API design, and data validation, done in collaboration with a class by Dr. Daniel G. Graham, PhD in the UVA School of Data Science.

---

## Features

- **RESTful Endpoint**: `POST /v1/survey` accepts survey responses in JSON format.
- **Data Validation**: Uses Pydantic to enforce field types and constraints:
  - `name` (string, 1–100 chars)
  - `email` (valid email)
  - `age` (integer, 13–120)
  - `consent` (boolean, default `true`)
  - `rating` (integer, 1–5)
  - Optional: `comments` (string, ≤1000 chars), `source` (`web`, `mobile`, `other`; default `other`)
- **Server-Enriched Fields**: Automatically logs `received_at` (UTC timestamp), `ip`, and `user_agent` (if available) for each submission.
- **Idempotency & Deduplication**: Supports submission IDs or generates a SHA256 hash from email + timestamp to avoid duplicate entries.
- **Append-Only Storage**: Stores each submission as a single line in NDJSON (`data/survey.ndjson`) for easy processing and analytics.
- **Observability & Privacy**:
  - Logs request metadata (status, latency, request_id) without exposing PII.
  - Supports metrics like submission counts, average rating, consent rate, and weekly volume.

---

## Tech Stack

- Python 3.11+
- Flask
- Pydantic
- Flask-CORS
- NDJSON storage

---

## Getting Started

### Installation

```bash
git clone https://github.com/yourusername/survey-intake-api.git
cd survey-intake-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### To Run the Server

```bash 
export FLASK_APP=app.py
flask run --port #add desired port here
```
## API Usage

### Example Request

```bash
curl -X POST http://localhost:1234/v1/survey \
-H "Content-Type: application/json" \
-d '{
  "name": "Alice Powell",
  "email": "alice@example.com",
  "age": 25,
  "consent": true,
  "rating": 5,
  "comments": "Great experience!",
  "source": "web"
}'
```

## Example Responses

- Success (201 Created)
- Bad Request (400) - Invalid JSON
- Unprocessable Entity (422) - Field validation error

### Project Structure

```bash
case4sept29/
├── app.py           # Flask application & routing
├── models.py        # Pydantic models for validation
├── storage.py       # NDJSON storage & deduplication logic
├── data/
│   └── survey.ndjson
├── frontend/        # Placeholder for frontend assets
├── tests/           # Minimal Flask test examples
├── .venv/           # Virtual environment
├── requirements.txt # Project dependencies (more seperatley installed in other files)
└── README.md        # Project documentation
```



