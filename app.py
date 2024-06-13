from datetime import datetime
import pandas as pd
import pytz
from flask import Flask, jsonify, request

app = Flask(__name__)

all_data = {
    "timelog": [],
    "Temperature C": [],
    "humidity": [],
}

@app.route("/")
def root_route():
    df = pd.DataFrame.from_dict(all_data)
    html_table = df.to_html()
    table_with_header = f"<h2>Temp and Humidity</h2>{html_table}"
    return table_with_header, 200

@app.route("/submit", methods=["GET"])
def submit_query():
    timestamp = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%d/%m/%Y %H:%M:%S")
    temp = float(request.args["temp"])
    hum = float(request.args["hum"])

    all_data["timestamp"].append(timestamp)
    all_data["temperature"].append(temp)
    all_data["humidity"].append(hum)
    return jsonify({
        "timestamp": timestamp,
        "temperature": temp,
        "humidity": hum,
    })

@app.route("/post", methods=["POST"])
def submit_post():
    timestamp = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%d/%m/%Y %H:%M:%S")
    data = request.get_json()
    temp = float(data["temp"])
    hum = float(data["hum"])

    all_data["timestamp"].append(timestamp)
    all_data["temperature"].append(temp)
    all_data["humidity"].append(hum)
    return jsonify({
        "timestamp": timestamp,
        "temperature": temp,
        "humidity": hum,
    })

if __name__ == "__main__":
    print("Temp and Humidity data")

    app.run(host='0.0.0.0', port=5000, debug=True)