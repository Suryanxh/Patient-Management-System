# Patient Management System

A simple FastAPI project that serves a frontend HTML page and provides a REST API for managing patient records.

## Project Structure

```bash
.
├── main.py
├── index.html
├── patients.json
├── requirements.txt
├── README.md
└── myenv/
```

## Features

- View all patients
- Get patient details by ID
- Create a new patient record
- Update an existing patient
- Delete a patient
- Sort records by height, weight, or BMI
- Frontend UI served from `index.html`

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

4. Open the app in your browser:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Get home message
```http
GET /
```

### Get about information
```http
GET /about
```

### Get all patients
```http
GET /view
```

### Get a patient by ID
```http
GET /patient/{patient_id}
```

### Create a patient
```http
POST /create
```

### Update a patient
```http
PUT /edit/{patient_id}
```

### Delete a patient
```http
DELETE /delete/{patient_id}
```

### Sort patients
```http
GET /sort?sort_by=height&order=asc
```

Available sort fields:
- `height`
- `weight`
- `bmi`

## Requirements

```txt
fastapi
uvicorn
pydantic
```

## Notes

- The app stores patient records in `patients.json`.
- The frontend is served from `index.html` and interacts with the FastAPI backend using API requests.
- CORS is enabled for frontend access.
