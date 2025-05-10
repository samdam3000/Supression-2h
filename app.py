from flask import Flask, jsonify
import time, requests
from bs4 import BeautifulSoup

app = Flask(__name__)

MATCH_URL = "https://www.foxsports.com.au/nrl/nrl-premiership/match-centre/NRL20251003"
API_ENDPOINT = "https://supression-sniper-2h.onrender.com"

def is_second_half():
    try:
        res = requests.get(MATCH_URL, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        clock_element = soup.select_one('.scoreboard__time')
        if not clock_element:
            return False, "Clock not found"

        time_str = clock_element.text.strip()
        if "2nd Half" in time_str or "2H" in time_str or "41:" in time_str or "50:" in time_str:
            return True, time_str
        return False, time_str
    except Exception as e:
        return False, str(e)

@app.route("/trigger")
def trigger():
    second_half, note = is_second_half()
    if second_half:
        return jsonify({
            "trigger": True,
            "confidence": "38.5%",
            "reason": "Second-half suppression reset window active",
            "note": note,
            "api": API_ENDPOINT
        })
    else:
        return jsonify({
            "trigger": False,
            "reason": "Not in second half window",
            "note": note,
            "api": API_ENDPOINT
        })

@app.route("/")
def health():
    return jsonify({"status": "2H Bot Live", "api": API_ENDPOINT})
