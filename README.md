# Appointment Scheduler Bot

This project is a simple NLP-based appointment scheduler built using Python and Flask.

It extracts:
- Date  
- Time  
- Department  
from natural language text.

---

## Features
- Accepts natural language input  
- Extracts appointment details  
- Handles relative dates like "tomorrow"  
- Returns structured JSON output  

---

## Tech Stack
- Python  
- Flask  
- python-dateutil  
- pytz  

---

## How to Run

1. Install dependencies

pip install -r requirements.txt

2. Run the app

python app.py

3. Test using PowerShell

Invoke-RestMethod -Uri http://127.0.0.1:5000/schedule `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text":"Eye checkup on 5 Feb at 10:30"}'

---

## Sample Output

{
  "appointment": {
    "date": "2026-02-05",
    "time": "10:30",
    "department": "Ophthalmology",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}
