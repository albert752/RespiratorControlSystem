from flask import Flask, render_template, request, jsonify
from utils.respirator import Respirator
import configparser

config = configparser.ConfigParser()
config.read("config.conf")



ID = config.get('Respirator', 'ID')
LOC = config.get('Respirator', 'LOC')

app = Flask(__name__)
respirator = Respirator(ID, LOC)

@app.route("/")
def home():
    return render_template('respirator.html', **respirator.get_info())

@app.route("/api/<param>")
def rest_api(param):
    if param == "status":
        return jsonify(respirator.get_info())
    else:
        return "Wrong api command"

if __name__ == "__main__":
    print("starting")
    respirator.start()
    print("hello")
    app.run(host="0.0.0.0", port=8000, debug=True)
