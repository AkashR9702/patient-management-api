# Patient Management API

A simple REST API built with FastAPI for managing patient records with automatic BMI calculation and health verdict classification.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Automatic BMI calculation using computed fields
- ✅ Health verdict classification (Underweight, Normal, Overweight, Obese)
- ✅ Sort patients by height, weight, or BMI
- ✅ Input validation with Pydantic
- ✅ JSON-based data storage

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Installation

1. Clone the repository
```bash
git clone https://github.com/AkashR9702/patient-management-api.git
cd patient-management-api
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the API

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

### GET Endpoints

- `GET /` - Welcome message
- `GET /about` - API information
- `GET /view` - Get all patients
- `GET /patient/{patient_id}` - Get specific patient by ID
- `GET /sort?sort_by=<field>&order=<asc|desc>` - Sort patients by height, weight, or BMI

### POST Endpoints

- `POST /create` - Create a new patient

**Request body:**
```json
{
  "id": "P001",
  "name": "John Doe",
  "city": "Mumbai",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

### PUT Endpoints

- `PUT /update/{patient_id}` - Update patient information (partial updates supported)

**Request body (all fields optional):**
```json
{
  "name": "John Updated",
  "city": "Delhi",
  "age": 31,
  "weight": 72
}
```

### DELETE Endpoints

- `DELETE /delete/{patient_id}` - Delete a patient record

## Example Usage

### Create a patient
```bash
curl -X POST "http://127.0.0.1:8000/create" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P001",
    "name": "Rahul Kumar",
    "city": "Bangalore",
    "age": 28,
    "gender": "male",
    "height": 1.70,
    "weight": 75
  }'
```

### Get all patients
```bash
curl "http://127.0.0.1:8000/view"
```

### Update a patient
```bash
curl -X PUT "http://127.0.0.1:8000/update/P001" \
  -H "Content-Type: application/json" \
  -d '{"weight": 73}'
```

### Delete a patient
```bash
curl -X DELETE "http://127.0.0.1:8000/delete/P001"
```

## BMI Classification

The API automatically calculates BMI and assigns health verdicts:

| BMI Range | Verdict |
|-----------|---------|
| < 18.5 | Underweight |
| 18.5 - 24.9 | Normal |
| 25.0 - 29.9 | Overweight |
| ≥ 30.0 | Obese |

## Project Structure

```
patient-management-api/
├── main.py              # FastAPI application
├── patients.json        # Data storage
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore file
└── README.md           # Documentation
```

## Learning Goals

This project was built to practice:
- FastAPI framework basics
- RESTful API design
- Pydantic data validation
- CRUD operations
- JSON file handling
- Computed fields and data modeling

## Future Improvements

- [ ] Add database support (SQLite/PostgreSQL)
- [ ] Add user authentication
- [ ] Add filtering and pagination


## 
