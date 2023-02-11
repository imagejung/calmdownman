import certifi
import bcrypt
import jwt

from pymongo import MongoClient

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from datetime import timedelta

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.0x2me9v.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.cdm

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    user = db.user.find_one({'id': id_receive})
    if user is not None:
        if bcrypt.checkpw(pw_receive.encode('UTF-8'), user['pw']) :
            return jsonify({'result': '로그인 성공!'});
        else:
            return jsonify({'result': 'pw가 틀렸습니다'});
    else:
        return jsonify({'result': 'id가 틀렸습니다'});

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/new', methods=['POST'])
def signup_new():
    id_receive = request.form['id_give']
    nickname_receive = request.form['nickname_give']
    pw_receive = request.form['pw_give']
    pw_pw_receive = request.form['pw_pw_give']

    if pw_receive != pw_pw_receive:
        return jsonify({'msg': '패스워드가 일치하지 않습니다!'})
    else:
        encoded_pw_receive = pw_receive.encode('utf-8')
        final_password = bcrypt.hashpw(encoded_pw_receive, bcrypt.gensalt())

        db.user.insert_one({'id': id_receive, 'pw': final_password, 'nick': nickname_receive})

        return jsonify({'result': 'success'})


# ID 중복확인
@app.route('/signup/check', methods=['POST'])
def signup_check():
    id_receive = request.form['id_give']

    check = db.user.find_one({'id': id_receive})

    if check is not None:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 아이디 입니다!'})
    elif check is False:
        return jsonify({'result': 'fail', 'msg': '사용가능한 아이디 입니다!'})
    else:
        return jsonify({'result': 'success'})

@app.route('/index')
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


@app.route("/write/get", methods=["GET"])
def write_get():
    write_list = list(db.write.find({}, {'_id': False}))
    return jsonify({'write_get':write_list})

@app.route('/detail/<int:num>')
def detail(num):
    title = db.write.find_one({'num':num})['title']
    image = db.write.find_one({'num':num})['image']
    comment = db.write.find_one({'num':num})['comment']
    star = db.write.find_one({'num':num})['star']
    url = db.write.find_one({'num':num})['url']
    num = db.write.find_one({'num':num})['num']
    return render_template('detail.html',num=num, title=title, image=image, comment=comment, star=star, url=url)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5004, debug=True)