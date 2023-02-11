import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)


import requests
from bs4 import BeautifulSoup

from datetime import timedelta 



ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.0x2me9v.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.cdm




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
        db.user.insert_one({'id': id_receive, 'pw': pw_receive, 'nick': nickname_receive})

        return jsonify({'result': 'success'})




# ID 중복확인
@app.route('/signup/check', methods=['POST'])
def signup_check():
    id_receive = request.form['id_give']

    check = db.user.find_one({'id': id_receive})

    if check is not None :
        return jsonify({ 'result':'fail','msg': '이미 존재하는 아이디 입니다!'})
    elif check is False:
        return jsonify({ 'result':'fail','msg': '사용가능한 아이디 입니다!'})
    else:
        return jsonify({'result':'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
