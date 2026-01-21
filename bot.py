from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# -----------------------------
# STEP 1: OCR / TEXT EXTRACTION
# -----------------------------
def ocr_text(input_text):
    return {
        "raw_text": input_text,
        "confidence": 0.90
    }

# -----------------------------
# STEP 2: ENTITY EXTRACTION
# -----------------------------
DEPARTMENT_MAP = {
    "dentist": "Dentist",
    "eye checkup": "Ophthalmology",
    "eye": "Ophthalmology",
    "ophthalmologist": "Ophthalmology",
    "hr": "Human Resources",
    "meeting": "Meeting"
}

def extract_entities(text):
    text_lower = text.lower()

    date_phrase = None
    time_phrase = None
    department = None

    # Date
    date_patterns = [
        r"next\s+\w+",
        r"tomorrow",
        r"\d{1,2}\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text_lower)
        if match:
            date_phrase = match.group()
            break

    # Time (supports 3pm, 10:30am, 10:30)
    time_match = re.search(r"\b\d{1,2}:\d{2}\b|\b\d{1,2}\s*(am|pm)\b", text_lower)
    if time_match:
        time_phrase = time_match.group().strip()

    # Department (check longest match first)
    for key in sorted(DEPARTMENT_MAP, key=len, reverse=True):
        if key in text_lower:
            department = key
            break

    if not date_phrase or not time_phrase or not department:
        return None, 0.50

    return {
        "date_phrase": date_phrase,
        "time_phrase": time_phrase,
        "department": department
    }, 0.85

# -----------------------------
# STEP 3: NORMALIZATION
# -----------------------------
def normalize_date(date_phrase):
    today = datetime.now()

    if date_phrase == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    if date_phrase.startswith("next"):
        day_name = date_phrase.replace("next", "").strip()
        days_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
        }

        if day_name.lower() in days_map:
            target_day = days_map[day_name.lower()]
            days_ahead = (target_day - today.weekday() + 7) % 7
            days_ahead = 7 if days_ahead == 0 else days_ahead
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    match = re.search(r"(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", date_phrase)
    if match:
        day = int(match.group(1))
        month_map = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }
        month = month_map[match.group(2)]
        year = today.year
        return f"{year:04d}-{month:02d}-{day:02d}"

    return None


def normalize_time(time_phrase):
    try:
        time_phrase = time_phrase.replace(" ", "").lower()

        # If no am/pm, assume AM
        if "am" not in time_phrase and "pm" not in time_phrase:
            time_phrase += "am"

        if ":" in time_phrase:
            dt = datetime.strptime(time_phrase, "%I:%M%p")
        else:
            dt = datetime.strptime(time_phrase, "%I%p")

        return dt.strftime("%H:%M")
    except:
        return None


def normalize_entities(entities):
    date = normalize_date(entities["date_phrase"])
    time = normalize_time(entities["time_phrase"])

    if not date or not time:
        return None, 0.50

    return {
        "date": date,
        "time": time,
        "tz": "Asia/Kolkata"
    }, 0.90

# -----------------------------
# STEP 4: FINAL APPOINTMENT JSON
# -----------------------------
def build_final_json(entities, normalized):
    return {
        "appointment": {
            "department": DEPARTMENT_MAP.get(
                entities["department"], entities["department"].title()
            ),
            "date": normalized["date"],
            "time": normalized["time"],
            "tz": normalized["tz"]
        },
        "status": "ok"
    }

# -----------------------------
# API ROUTE
# -----------------------------
@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"status": "error", "message": "Missing text"}), 400

    input_text = data["text"]

    # Step 1
    step1 = ocr_text(input_text)

    # Step 2
    entities, entities_conf = extract_entities(step1["raw_text"])
    if not entities:
        return jsonify({"status": "needs_clarification", "message": "Ambiguous date/time or department"})

    step2 = {
        "entities": entities,
        "entities_confidence": entities_conf
    }

    # Step 3
    normalized, norm_conf = normalize_entities(entities)
    if not normalized:
        return jsonify({"status": "needs_clarification", "message": "Could not normalize date/time"})

    step3 = {
        "normalized": normalized,
        "normalization_confidence": norm_conf
    }

    # Step 4
    step4 = build_final_json(entities, normalized)

    return jsonify({
        "step1_ocr": step1,
        "step2_entities": step2,
        "step3_normalized": step3,
        "step4_final": step4
    })

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
