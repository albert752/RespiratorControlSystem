from flask import Flask, render_template, request, jsonify
from utils.breather import Breather
import configparser

config = configparser.ConfigParser()
config.read("config.conf")



ID = config.get('Breather', 'ID')
LOC = config.get('Breather', 'LOC')

app = Flask(__name__)
breather = Breather(ID, LOC)

@app.route("/")
def home():
    return render_template('breather.html', **breather.get_info())

@app.route("/api/<param>")
def rest_api(param):
    if param == "status":
        return jsonify(breather.get_info())
    else:
        return "Wrong api command"

if __name__ == "__main__":
    print("starting")
    breather.start()
    print("hello")
    app.run(host="localhost", port=80, debug=True)
