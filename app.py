from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

from pymongo import MongoClient
import certifi

import requests
from bs4 import BeautifulSoup

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.0x2me9v.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.cdm

import jwt
import hashlib
import datetime

@app.route('/')
def home():
    return render_template('login.html')

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup/new', methods=['POST'])
def signup_new():
    id_receive = request.form['id_give']
    nickname_receive = request.form['nickname_give']
    pw_receive = request.form['pw_give']
    pw_pw_receive = request.form['pw_pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()


    if pw_receive != pw_pw_receive:
        return jsonify({'msg': '패스워드가 일치하지 않습니다!'})
    else:

        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

        return jsonify({'result': 'success'})


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

@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
