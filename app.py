from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>This is Cost Cannabis Test Backend!</p>"