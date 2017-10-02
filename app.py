import requests
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return requests.get('http://52.187.51.158:8082/mongodb/boschxdk03/latestdata').content

