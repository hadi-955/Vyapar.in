import json, datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_data(device_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "success": True,
        "message": "OK",
        "data": {
            "deviceId": device_id,
            "licenseStatus": "ACTIVE",
            "businessStatus": "ACTIVE",
            "plan": "POS",
            "planName": "Vyapar POS",
            "trialDaysLeft": 9999,
            "trialExpired": False,
            "expiryDate": "2999-12-31 23:59:59",
            "billingAllowed": True,
            "syncAllowed": True,
            "onlineBackup": True,
            "lastUpdated": now,
            "features": {
                "gst": True,
                "inventory": True,
                "multi_user": True,
                "reports": True
            }
        }
    }

    return jsonify(data)


@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
def api_old(device_id):
    return get_data(device_id)


@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def api_new(device_id):
    return get_data(device_id)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    base = 'https://vyaparapp.in/'

    if request.method == 'GET':
        return requests.get(base + path).text
    else:
        return requests.post(base + path, data=request.form).text
