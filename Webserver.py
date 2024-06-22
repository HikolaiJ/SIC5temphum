from datetime import datetime
import pandas as pd
import pytz
from flask import Flask, jsonify, request

#All comments are written by Mahya Byantara
app = Flask(__name__)

#Data tables
all_data = {
    "timelog": [],
    "Temperature C": [],
    "humidity": [],
    "moisture": [],
}

@app.route("/")
def root_route():
    df = pd.DataFrame.from_dict(all_data)
    html_table = df.to_html()
    table_with_header = f"<h2>Temp, Humidity, and Moiture</h2>{html_table}" #HTML elements
    return table_with_header, 200

#time log
@app.route("/submit", methods=["GET"]) #Submit time, humidity and temperature
def submit_query():
    timestamp = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%d/%m/%Y %H:%M:%S")
    temp = float(request.args["temp"])
    hum = float(request.args["hum"])
    mos = float(request.args["mos"])

    all_data["timestamp"].append(timestamp)
    all_data["temperature"].append(temp)
    all_data["humidity"].append(hum)
    all_data["moisture"].append(mos)
    return jsonify({
        "timestamp": timestamp,
        "temperature": temp,
        "humidity": hum,
        "moisture": mos,
    })

@app.route("/post", methods=["POST"])
def submit_post():
    timestamp = datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime("%d/%m/%Y %H:%M:%S")
    data = request.get_json()
    temp = float(data["temp"])
    hum = float(data["hum"])
    mos = float(data["mos"])

    all_data["timestamp"].append(timestamp)
    all_data["temperature"].append(temp)
    all_data["humidity"].append(hum)
    return jsonify({
        "timestamp": timestamp,
        "temperature": temp,
        "humidity": hum,
        "moisture": mos,
    })

if __name__ == "__main__":
    print("Temp and Humidity data")

    app.run(host='0.0.0.0', port=5000, debug=True)
