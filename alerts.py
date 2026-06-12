from datetime import datetime
from pathlib import Path

LOG_FILE = "logs/alerts.log"


def create_alert(message):

    Path("logs").mkdir(exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a") as f:
        f.write(
            f"[{timestamp}] {message}\n"
        )


def log_fault(data):

    create_alert(
        f"FAULT DETECTED | "
        f"Temp={data['temperature']}°C | "
        f"Vibration={data['vibration']} | "
        f"Current={data['current']}A"
    )


def log_attack(data):

    create_alert(
        f"CYBER ATTACK | "
        f"Reported Temp={data['temperature']}°C | "
        f"Actual Temp={data['actual_temperature']}°C"
    )