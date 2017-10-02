import requests
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    data = requests.get('http://52.187.51.158:8082/mongodb/boschxdk03/latestdata').json()
    return jsonify({key:value for key,value in data.items() if key in ['noiselevel','temperature','humidity','millilux']})

