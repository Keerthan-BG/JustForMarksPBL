from flask import Flask, render_template, jsonify
from alerts import log_fault, log_attack

app = Flask(__name__)

history = {
    "temperature": [50, 52, 54, 55, 56],
    "vibration": [10, 11, 10, 12, 11],
    "current": [4, 4.1, 4.2, 4.3, 4.2]
}


def get_data(mode="normal"):

    if mode == "fault":
        return {
            "temperature": 110,
            "vibration": 30,
            "current": 12
        }

    elif mode == "attack":
        return {
            "temperature": 60,
            "actual_temperature": 115,
            "vibration": 30,
            "current": 12
        }

    return {
        "temperature": 50,
        "vibration": 10,
        "current": 4
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data/<mode>")
def api(mode):

    data = get_data(mode)

    history["temperature"].append(data["temperature"])
    history["vibration"].append(data["vibration"])
    history["current"].append(data["current"])

    for key in history:
        history[key] = history[key][-20:]

    health = 100

    health -= data["temperature"] * 0.4
    health -= data["vibration"] * 1.5
    health -= data["current"] * 3

    health = max(5, int(health))

    rul = max(5, int(health * 1.5))

    if mode == "fault":
        log_fault(data)

    elif mode == "attack":
        log_attack(data)

    return jsonify({
        "data": data,
        "history": history,
        "health": health,
        "rul": rul,
        "mode": mode
    })


@app.route("/api/logs")
def logs():

    try:

        with open("logs/alerts.log", "r") as f:
            lines = f.readlines()[-20:]

        return jsonify({
            "logs": lines
        })

    except:
        return jsonify({
            "logs": []
        })


if __name__ == "__main__":
    app.run(debug=True)