from flask import Flask, render_template, request, jsonify
from motor import Motor
from breather import Breather

app = Flask(__name__)
breather = Breather("123", "SF34")

@app.route("/")
def home():
    return render_template('breather.html', **breather.get_info())

@app.route("/api/<param>")
def rest_api(param):
    if param == "status":
        return jsonify(context)
    else:
        return "Wrong api command"

if __name__ == "__main__":
    breather.start()
    app.run(host="localhost", port=80, debug=True)
