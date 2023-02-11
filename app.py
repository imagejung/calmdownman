import certifi
from pymongo import MongoClient

import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.0x2me9v.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.cdm

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/write/post", methods=["POST"])
def write_post():
    star_receive = request.form['star_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title_receive = soup.select_one('meta[property="og:title"]')['content']
    image_receive = soup.select_one('meta[property="og:image"]')['content']
    desc_receive = soup.select_one('meta[property="og:description"]')['content']

    title_list = list(db.write.find({}, {'id': False}).sort("num", -1).limit(1))
    url_list = list(db.write.find({}, {'id': False}).sort("num", -1).limit(1))
    comment_list = list(db.write.find({}, {'id': False}).sort("num", -1).limit(1))

    if len(title_list) == 0: count = 1
    else : count = title_list[0]['num'] + 1

    doc = {
            'num':count,
            'star':star_receive,
            'url':url_receive,
            'comment':comment_receive,
            'title':title_receive,
            'image':image_receive,
    }

    db.write.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/detail/<param>")
def detail(param):
    return render_template("detail.html", param=param)

@app.route("/detail/<param>", methods=["POST"])
def get_data(param):
    num = param
    print(num, file=sys.stderr)
    detail_data = db.write.find_one({'num': num}, {'_id': False})
    return jsonify({'data': detail_data})

@app.route("/write/get", methods=["GET"])
def write_get():
    write_list = list(db.write.find({}, {'_id': False}))
    return jsonify({'write_get':write_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
