from flask import Flask, jsonify, request, render_template
import json
import subprocess
from datetime import datetime
import pytz

app = Flask(__name__)

def run_speedtest():
    try:
        result = subprocess.run(["speedtest", "--json"], capture_output=True, text=True)
        return {"data": json.loads(result.stdout)}
    except Exception as e:
        return {"error": f"Speedtest CLI error: {str(e)}"}

def convert_to_local_time(utc_time, timezone):
    try:
        utc_datetime = datetime.fromisoformat(utc_time.replace("Z", "+00:00"))
        local_tz = pytz.timezone(timezone)
        local_datetime = utc_datetime.astimezone(local_tz)
        return local_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"Error converting time: {str(e)}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start-test', methods=['POST'])
def start_test():
    timezone = request.json.get("timezone", None)
    if not timezone:
        return jsonify({"error": "Timezone not provided"}), 400

    result = run_speedtest()
    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    data = result["data"]
    data["timestamp"] = convert_to_local_time(data["timestamp"], timezone)

    return jsonify({
        "download_speed": f"{data['download'] / 1_000_000:.2f} Mbps",
        "upload_speed": f"{data['upload'] / 1_000_000:.2f} Mbps",
        "ping": f"{data['ping']} ms",
        "server_name": data["server"]["name"],
        "server_country": data["server"]["country"],
        "server_host": data["server"]["host"],
        "timestamp": data["timestamp"],
        "client_ip": data["client"]["ip"],
        "isp": data["client"]["isp"]
    })

if __name__ == '__main__':
    app.run(debug=True)
