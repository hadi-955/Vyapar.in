import json, datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------------- License Data ----------------
def get_license_data(device_id="UNKNOWN"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "success": True,
        "message": "OK",
        "data": {
            "deviceId": device_id,
            "licenseStatus": "ACTIVE",
            "businessStatus": "ACTIVE",
            "plan": "PLATINUM",
            "planName": "Vyapar Platinum",
            "trialDaysLeft": 9999,
            "trialExpired": False,
            "expiryDate": "2099-12-31 23:59:59",
            "billingAllowed": True,
            "syncAllowed": True,
            "onlineBackup": True,
            "features": {
                "gst": True,
                "inventory": True,
                "multi_user": True,
                "reports": True,
                "cloud_sync": True,
            },
            "current_date": now
        }
    }

# ---------------- License Endpoints ----------------
@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def license_api(device_id):
    return jsonify(get_license_data(device_id))

# Optional additional endpoints Vyapar may call internally
@app.route('/license/info', methods=['GET'])
@app.route('/license/details', methods=['GET'])
def license_info():
    return jsonify(get_license_data("INTERNAL"))

# ---------------- Catch-All Proxy ----------------
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f'https://vyaparapp.in/{path}'
    try:
        if request.method == 'POST':
            r = requests.post(url, data=request.form, timeout=10)
        else:
            r = requests.get(url, timeout=10)
        return r.text
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Proxy failed", "details": str(e)}), 502

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
