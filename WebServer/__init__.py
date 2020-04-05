#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
from utils.respirator import Respirator
import configparser
import os

ID = 123
LOC = "Hab 123"

app = Flask(__name__)
respirator = Respirator(ID, LOC)

@app.route("/api/<param>")
def rest_api(param):
    return jsonify(respirator.get_info())

if __name__ == "__main__":
    respirator.start()
    app.run()
