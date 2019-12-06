from flask import Flask,render_template,request,jsonify,redirect,send_from_directory
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask_mongoengine import MongoEngine
from models import *
import os
import json
import random
import pymysql
import database

db = pymysql.connect("localhost", "root", "flamer", "mydb")
cursor = db.cursor()

app=Flask(__name__,template_folder="template",static_folder="static")
app.config.from_object("config")

loginmanager=LoginManager(app)
loginmanager.session_protection="strong"
loginmanager.login_view="login"

# db=MongoEngine(app)

basedir=os.path.abspath(os.path.dirname(__file__))
download_floder=os.path.join(basedir,"upload")


def url_list(filename):
    return "<li><a href='{}'>{}</a><input style='float:right' type='button' id='{}' value='删除' onclick='delete_file(event)'></li>".format("/download/"+filename,filename,filename)


@loginmanager.user_loader
def get_user(user_id):
    user = database.Search(cursor, "mydb.users", "id", user_id)
    user_class = User(user)
    return user_class


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@login_required
def home_0():
    return render_template("home.html")


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        err_msg={
            "result":"NO"
        }
        param = json.loads(request.data.decode("utf-8"))
        username = param.get('username')
        password = param.get('password')
        if username is "":
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if password is "":
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        user = database.Search(cursor, "mydb.users", "username", username)
        if len(user) is 0:
            err_msg["msg"] = "用户尚未注册"
            return jsonify(err_msg)
        user_class = User(user)
        if not user_class.verify_password(password):
            err_msg["msg"] = "密码错误"
            return jsonify(err_msg)
        login_user(user_class)
        return jsonify({
            "result": "OK",
            "next_url": "/"
        })


@app.route("/abnormal")
def abnormal():
    return render_template("abnormal.html")


@app.route("/complete")
def complete():
    return render_template("complete.html")


@app.route("/department")
def department():
    return render_template("department.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/media")
def media():
    return render_template("media.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/nature")
def nature():
    return render_template("nature.html")


@app.route("/table")
def table():
    return render_template("table.html")


@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    elif request.method=="POST":
        err_msg = {
            "result": "NO"
        }
        param = json.loads(request.data.decode("utf-8"))
        print(param)
        firstname = param.get('firstname')
        lastname = param.get('lastname')
        username = param.get('username')
        GM = param.get('GM')
        # NGM = param.get('NGM')
        password = param.get('password')
        repassword = param.get('repassword')
        if firstname is None:
            err_msg["msg"] = "缺少姓"
            return jsonify(err_msg)
        if lastname is None:
            err_msg["msg"] = "缺少名"
            return jsonify(err_msg)
        if username is None:
            err_msg["msg"] = "缺少用户名"
            return jsonify(err_msg)
        if GM is None:
            return jsonify(err_msg)
        if password is None:
            err_msg["msg"] = "缺少密码"
            return jsonify(err_msg)
        if repassword is None:
            err_msg["msg"] = "未重复输入密码"
            return jsonify(err_msg)
        if password != repassword:
            err_msg["msg"] = "密码两次不一致"
            return jsonify(err_msg)
        user = database.Search(cursor, "mydb.users", "username", username)
        if len(user) == 0:
            user_id = len(database.Search(cursor, "mydb.users")) + 1
            user_class = User(((user_id, firstname, lastname, username, GM, password),))
            user_class.hash_password(password)
            user = (user_id, firstname, lastname, username, GM, user_class.password_hash)
            database.Insert(db, "mydb.users", user)
            return jsonify({
                "result": "OK"
            })
        else:
            err_msg["msg"]="用户已经注册"
            return jsonify(err_msg)
        return jsonify({
            "result": "OK",
            "next_url": "/"
       })

@app.route('/')
def my_echart():
    #在浏览器上渲染模板
    return render_template('sample3.html')

# /data路由接收前端的ajax请求
@app.route('/data_index',methods=["POST","GET"])
def my_echart_data():
    # 连接数据库，从数据库中获取数据
    if request.method == "POST":
        err_msg = {
            "result": "NO"
        }
        conn = pymysql.connect("localhost", "root", "flamer", "mydb")
        cursor = conn.cursor()
        cursor.execute('select * from mydb.data_event')
        datas = cursor.fetchall()
        # 创建一个空数组，将sql返回的数据进行逐个存到这个数组里面
        jsondata = {}
        xd = [[0 for i in range(6)] for i in range(134)]
        param = json.loads(request.data.decode("utf-8"))
        time = param.get('time')
        for data in datas:
            if time in data[16] and data[24] != '-' and data[15] != '-':
                xd[MAIN_TYPE_NAME[data[24]]][STREET_NAME[data[15]]] += 1

        for i in range(92):
            jsondata['data'+str(i)] = xd[i]
        # 将结果转化为json格式
        jsondata['result'] = 'OK'
        j = jsonify(jsondata)
        cursor.close()
        conn.close()
        return j

@app.route('/data_department',methods=["POST","GET"])
def my_echart_data_department():
    # 连接数据库，从数据库中获取数据
    if request.method == "POST":
        err_msg = {
            "result": "NO"
        }
        conn = pymysql.connect("localhost", "root", "flamer", "mydb")
        cursor = conn.cursor()
        cursor.execute('select * from mydb.data_event')
        datas = cursor.fetchall()
        # 创建一个空数组，将sql返回的数据进行逐个存到这个数组里面
        jsondata = {}
        x = [[0] for i in range(len(COMMUNITY_NAME))]
        param = json.loads(request.data.decode("utf-8"))
        time = param.get('time')
        for data in datas:
            if time in data[16] and data[22] != '-':
                x[COMMUNITY_NAME[data[22]]][0] += 1
        for i in range(len(COMMUNITY_NAME)):
            jsondata['data'+str(i)] = x[i]
        jsondata['result'] = 'OK'
        # 将结果转化为json格式
        j = jsonify(jsondata)
        cursor.close()
        conn.close()
        return j

@app.route('/data_nature',methods=["POST","GET"])
def my_echart_data_nature():
    # 连接数据库，从数据库中获取数据
    if request.method == "POST":
        err_msg = {
            "result": "NO"
        }
        conn = pymysql.connect("localhost", "root", "flamer", "mydb")
        cursor = conn.cursor()
        cursor.execute('select * from mydb.data_event')
        datas = cursor.fetchall()
        # 创建一个空数组，将sql返回的数据进行逐个存到这个数组里面
        jsondata = {}
        x = [[0] for i in range(6)]
        param = json.loads(request.data.decode("utf-8"))
        time1 = param.get('time1')
        time2 = param.get('time2')
        for data in datas:
            if time1 > time2:
                err_msg["msg"] = "起始时间晚于初始时间"
                return jsonify(err_msg)
            elif (time1 <= data[16] or time1 is "") and (time2 >= data[16] or time2 is ""):
                x[EVENT_PROPERTY_NAME[data[1]]][0] += 1
        for i in range(6):
            jsondata['data'+str(i)] = x[i]
        jsondata['result'] = 'OK'
        # 将结果转化为json格式
        j = jsonify(jsondata)
        cursor.close()
        conn.close()
        return j

@app.route('/data_complete',methods=["POST","GET"])
def my_echart_data_complete():
    # 连接数据库，从数据库中获取数据
    if request.method == "POST":
        conn = pymysql.connect("localhost", "root", "flamer", "mydb")
        cursor = conn.cursor()
        cursor.execute('select * from mydb.data_event')
        datas = cursor.fetchall()
        err_msg = {
            "result": "NO"
        }
        jsondata = {}
        d = [[0] for i in range(len(EVENT_TYPE_NAME))]
        cate = [0,0,0]
        param = json.loads(request.data.decode("utf-8"))
        time1 = param.get('time1')
        time2 = param.get('time2')
        for data in datas:
            if time1 > time2:
                err_msg["msg"] = "起始时间晚于初始时间"
                return jsonify(err_msg)
            elif (time1 <= data[16] or time1 is "") and (time2 >= data[16] or time2 is ""):
                if data[12]:
                    cate[0] += 1
                elif data[18]:
                    cate[1] += 1
                elif data[6]:
                    cate[2] += 1
                if data[3] != '-':
                    d[EVENT_TYPE_NAME[data[3]]][0] += 1
        for i in range(len(cate)):
            jsondata['cate'+str(i)] = cate[i]
        for i in range(len(d)):
            jsondata['data'+str(i)] = d[i]
        # 将结果转化为json格式
        jsondata['result'] = 'OK'
        j = jsonify(jsondata)
        cursor.close()
        conn.close()
        return j

@app.route('/data_abnormal',methods=["GET"])
def my_echart_data_abnormal():
    if request.method == "GET":
        conn = pymysql.connect("localhost", "root", "flamer", "mydb")
        cursor = conn.cursor()
        cursor.execute('select * from mydb.data_event')
        datas = cursor.fetchall()
        # 创建一个空数组，将sql返回的数据进行逐个存到这个数组里面
        jsondata = {}
        d = []
        cate = [0, 0, 0]
        for data in datas:
            if "2018-10-30" in data[16]:
                d.append([data[15], data[24], data[19], data[1]])
        for i in range(len(d)):
            jsondata['data'+str(i)] = d[i]
        # 将结果转化为json格式
        j = jsonify(d)
        cursor.close()
        conn.close()
        return j

if __name__=='__main__':
    if not os.path.exists(download_floder):
        os.makedirs(download_floder)
    app.run()