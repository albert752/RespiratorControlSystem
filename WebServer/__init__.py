#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from utils.respirator import Respirator
import os
from uuid import getnode

config = {  
            "Respirator": {
                "ID": hex(getnode())[2:].upper()
                "LOC": "Not set",
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
def status():
    return jsonify(respirator.get_info())

@app.route("/api/loc", methods=['POST'])
def location():
    try:
        respirator.set_loc(request.json['loc'])
        info = respirator.get_info()
    except:
        info = {"error": "Location not changed"}
    return jsonify(info)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
