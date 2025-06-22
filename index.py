import json
import datetime
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# ───────────────────────────────────────────────────────────────
# ⏱️ Get Current License Data
# ───────────────────────────────────────────────────────────────
def get_license_data():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "license_code": "Hasnain Ali",
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

# ───────────────────────────────────────────────────────────────
# 📤 Add Custom Response Headers
# ───────────────────────────────────────────────────────────────
def add_headers(response):i
    response.headers['Content-Type'] = 'application/json'
    response.headers['Server'] = 'Pro_Max_Futuristics'
    response.headers['Custom-Header'] = 'Pro_Max'
    return response

# ───────────────────────────────────────────────────────────────
# 🎯 License API (old and new)
# ───────────────────────────────────────────────────────────────
@app.route('/api/license/<device_id>', methods=['GET', 'POST'])
@app.route('/api/ns/license/<device_id>', methods=['GET', 'POST'])
def license_api(device_id):
    response = make_response(jsonify(get_license_data()))
    return add_headers(response)

# ───────────────────────────────────────────────────────────────
# 🌐 Proxy to vyaparapp.in
# ───────────────────────────────────────────────────────────────
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy_handler(path):
    url = f'https://vyaparapp.in/{path}'

    try:
        if request.method == 'POST':
            proxied = requests.post(url, data=request.form, timeout=10)
        else:
            proxied = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return add_headers(make_response(jsonify(error="Proxy Request Failed", detail=str(e)), 502))

    content_type = proxied.headers.get('Content-Type', '')

    # Only allow JSON responses
    if 'application/json' in content_type:
        try:
            data = proxied.json()
        except ValueError:
            return add_headers(make_response(jsonify(error="Malformed JSON from origin server"), 502))
        return add_headers(make_response(jsonify(data)))
    else:
        return add_headers(make_response(jsonify(error="Upstream server did not return JSON"), 502))

# ───────────────────────────────────────────────────────────────
# ❌ Custom Error Handlers
# ───────────────────────────────────────────────────────────────
@app.errorhandler(404)
def handle_404(e):
    return add_headers(make_response(jsonify(error="Not Found"), 404))

@app.errorhandler(500)
def handle_500(e):
    return add_headers(make_response(jsonify(error="Internal Server Error"), 500))

# ───────────────────────────────────────────────────────────────
# ▶️ Entry Point
# ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
