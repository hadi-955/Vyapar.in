import json, datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_data():
    date = datetime.datetime.now()
    currentdt = date.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "license_code": "Taste 1",
        "expiry_date": "2026-12-31 23:59:59",
        "plan": "Pos",
        "planId": 166,
        "status": 2,
        "created_at": "2022-01-01 00:00:00",
        "current_date": currentdt,
        "groupTitle": None,
        "planType": 3,
        "perDayCost": 0,
        "perDayCostUsd": 0,
        "pairExpiryDate": "2026-12-31 23:59:59"
    }
    return jsonify(data)

@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
def api_old(device_id):
    return get_data()

@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def api_new(device_id):
    return get_data()
import requests
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        r = requests.get('https://vyaparapp.in/' + path)
        return r.text
    elif request.method == 'POST':
        r = requests.post('https://vyaparapp.in/' + path, data=request.form)
        return r.text
