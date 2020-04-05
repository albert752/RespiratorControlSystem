#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from utils.respirator import Respirator
import os

config = {  
            "Respirator": {
                "ID": "123",
                "LOC": "SF45",
                "POLL_FREQ": 1
            },
            "Motor": {
                "STARTUP_TIME": 60,
                "MIN_RPM_MOTOR": 12,
                "MAX_RPM_MOTOR": 35,
                "MAX_DIFF_SAMPLES": 6
            }
        }
respirator = Respirator(config)
respirator.start()

app = Flask(__name__)

@app.route("/api/status")
def rest_api():
    return jsonify(respirator.get_info())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
