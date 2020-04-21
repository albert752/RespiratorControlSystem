#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from utils.respirator import Respirator
import os
from uuid import getnode

with open('/var/www/WebServer/location.txt', 'r') as fp:
    loc = fp.read().replace('\n', '')
    fp.close()

config = {  
            "Respirator": {
                "ID": hex(getnode())[2:].upper(),
                "LOC":loc,
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
cors = CORS(app)

@app.route("/api/status")
@cross_origin()
def status():
    return jsonify(respirator.get_info())

@app.route("/api/loc", methods=['POST'])
@cross_origin()
def location():
    try:
        respirator.set_loc(request.json['loc'])
        with open('/var/www/WebServer/location.txt', 'w') as fp:
            fp.write(request.json['loc'])
            fp.close()
        info = respirator.get_info()
    except:
        info = {"error": "Location not changed"}
    return jsonify(info)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
