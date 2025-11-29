import json
import datetime
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


# ------------------ License Function ------------------
def get_data():
    currentdt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "license_code": "Hasnain Ali",
        "expiry_date": "2999-12-31 23:59:59",
        "plan": "Pos",
        "planId": 166,
        "status": 2,
        "created_at": "2022-01-01 00:00:00",
        "current_date": currentdt,
        "groupTitle": None,
        "planType": 3,
        "perDayCost": 0,
        "perDayCostUsd": 0,
        "pairExpiryDate": "2999-12-31 23:59:59"
    }

    return jsonify(data)



# ------------------ License Routes ------------------
@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
def api_old(device_id):
    return get_data()

@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def api_new(device_id):
    return get_data()



# ------------------ SAFE PROXY ROUTE ------------------
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    url = f"https://vyaparapp.in/{path}"

    try:
        if request.method == 'GET':
            r = requests.get(url, timeout=5)
            return r.text

        elif request.method == 'POST':
            r = requests.post(url, data=request.form, timeout=5)
            return r.text

    except Exception as e:
        return jsonify({
            "error": "Proxy Failed",
            "details": str(e),
            "path": path
        })
