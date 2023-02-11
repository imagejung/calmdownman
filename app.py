import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.0x2me9v.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
