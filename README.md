# Plum Appointment Scheduler

AI-powered appointment scheduling backend built using Python and Flask.  
This project converts natural language text into structured appointment data using a multi-step processing pipeline.

## 🚀 Features

- Accepts free-text appointment requests
- Extracts date, time, and department from text
- Normalizes date and time into standard format
- Returns structured JSON output
- REST API built with Flask

## 🛠️ Tech Stack

- Python 3  
- Flask  
- python-dateutil  
- pytz  

## 📂 Project Structure

plum-appointment-scheduler/
├── bot.py  
├── requirements.txt  
└── README.md  

## ▶️ How to Run the Project

1. Clone the repository:

git clone https://github.com/Nehaspatil1219/plum-appointment-scheduler.git  
cd plum-appointment-scheduler  

2. Install dependencies:

pip install -r requirements.txt  

3. Run the Flask server:

python bot.py  

4. The API will start at:

http://127.0.0.1:5000  

## 🧪 Example API Request

Send a POST request to:

POST /schedule  

With JSON body:

{
  "text": "Eye checkup on 5 Feb at 10:30"
}

## 📤 Example Response

{
  "appointment": {
    "date": "2026-02-05",
    "time": "10:30",
    "department": "Ophthalmology",
    "tz": "Asia/Kolkata"
  },
  "status": "ok"
}

## 🎯 Learning Outcome

- Built REST APIs using Flask  
- Implemented entity extraction and normalization  
- Worked with date-time parsing and time zones  
- Designed multi-step NLP-style processing pipeline  

