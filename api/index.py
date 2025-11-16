import json
import datetime
import requests
from flask import Flask, request, jsonify, make_response, Response

app = Flask(__name__)

# ───────────────────────────────────────────────
# License Function
# ───────────────────────────────────────────────
def get_license_data():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "license_code": "C0DE_Li0N",
        "expiry_date": "2999-12-31 23:59:59",
        "plan": "Pos",
        "planId": 166,
        "status": 2,
        "created_at": "2022-01-01 00:00:00",
        "current_date": now,
        "groupTitle": None,
        "planType": 3,
        "perDayCost": 0,
        "perDayCostUsd": 0,
        "pairExpiryDate": "2999-12-31 23:59:59"
    }

# ───────────────────────────────────────────────
# Add headers
# ───────────────────────────────────────────────
def add_headers(response):
    response.headers['Server'] = 'Pro_Max_Futuristics'
    response.headers['Custom-Header'] = 'Pro_Max'
    return response

# ───────────────────────────────────────────────
# License Routes
# ───────────────────────────────────────────────
@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def license_api(device_id):
    return add_headers(make_response(jsonify(get_license_data())))

# ───────────────────────────────────────────────
# Allow FULL Sync Support
# ───────────────────────────────────────────────
@app.route('/sync/<path:path>', methods=['GET', 'POST'])
def sync_proxy(path):

    url = f"https://vyaparapp.in/sync/{path}"

    try:
        if request.method == "POST":
            proxied = requests.post(url, data=request.data, headers=request.headers, timeout=20)
        else:
            proxied = requests.get(url, headers=request.headers, timeout=20)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Sync proxy failed", "detail": str(e)}), 502

    return Response(
        proxied.content,
        status=proxied.status_code,
        content_type=proxied.headers.get("Content-Type")
    )

# ───────────────────────────────────────────────
# Full Proxy (fallback)
# ───────────────────────────────────────────────
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def full_proxy(path):

    url = f"https://vyaparapp.in/{path}"

    try:
        if request.method == "POST":
            proxied = requests.post(url, data=request.data, headers=request.headers, timeout=20)
        else:
            proxied = requests.get(url, headers=request.headers, timeout=20)

    except Exception as e:
        return jsonify({"error": "Proxy failed", "detail": str(e)}), 500

    return Response(
        proxied.content,
        status=proxied.status_code,
        content_type=proxied.headers.get("Content-Type")
    )


# ───────────────────────────────────────────────
# Run
# ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
