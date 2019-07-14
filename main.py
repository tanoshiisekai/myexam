from gevent import monkey
monkey.patch_all()
import conf
from flask import render_template
import dbtools
from flask import Flask
from flask import request, redirect, make_response
from dbtools import app
from flask import jsonify
from info import Info
import logiclayer
from werkzeug.utils import secure_filename
from flask import url_for
import os
import uuid
import datetime
import hashlib
import tools


@app.route("/doinitstudents", methods=["GET"])
def doinitstudents():
    return jsonify(logiclayer.initstudents())


@app.route("/removeip", methods=["GET"])
def removeip():
    remoteip = request.remote_addr
    username = request.cookies.get("username")
    if logiclayer.removestudentip(username, remoteip):
        return jsonify(Info(True, "成功退出系统").todict())
    else:
        return jsonify(Info(False, "数据库异常").todict())


@app.route("/finished", methods=["POST"])
def finished():
    remoteip = request.remote_addr
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        userright = request.form["user_right"]
        userwrong = request.form["user_wrong"]
        timestart = request.form["timestart"]
        timeend = request.form["timeend"]
        userchoicelog = request.form["userchoicelog"]
        secret = request.form["secret"]
        token = request.form["token"]
        key = timeend
        strmsg = str(userright) + str(userwrong) + str(timestart) + str(timeend) + str(userchoicelog)
        checksecret = tools.getsecretstr(strmsg, key)
        if secret != checksecret:
            return jsonify(Info(False, "成绩被篡改，请重新答题！secret").todict())
        else:
            if logiclayer.checkusertoken(username, token):
                if logiclayer.removestudentip(username, remoteip):
                    dt1 = datetime.datetime(*[int(x) for x in timestart.split("_")])
                    dt2 = datetime.datetime(*[int(x) for x in timeend.split("_")])
                    timeduring = (dt2-dt1).seconds
                    return jsonify(logiclayer.updateuser(username, userright, userwrong, timeduring, userchoicelog))
                else:
                    return jsonify(Info(False, "数据库异常").todict())
            else:
                return jsonify(Info(False, "成绩被篡改，请重新答题！token").todict())
    else:
        return redirect("/")



@app.route("/getproblembyid", methods=["GET"])
def getproblembyid():
    idstr = request.args.get("problemid");
    return jsonify(logiclayer.getproblembyid(idstr))


@app.route("/getproblemsid", methods=["GET"])
def getproblemsid():
    problemlist = logiclayer.getrandomproblemlist()
    if problemlist:
        return jsonify(Info(True, "题目获取成功", {"problemlist":problemlist}).todict())
    else:
        return jsonify(Info(False, "数据库中没有题目").todict())


@app.route("/exam", methods=["GET"])
def exam():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        return render_template('exam.html', username=username)
    else:
        return redirect("/")


@app.route("/adminlogin", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/", methods=["GET"])
def student():
    return render_template('studentlogin.html')


@app.route("/studentlogin", methods=["POST"])
def studentlogin():
    username = request.form["username"]
    password = request.form["password"]
    remoteip = request.remote_addr
    if logiclayer.checkstudentip(username, remoteip):
        if logiclayer.updatestudentip(username, remoteip):
            if logiclayer.checkstudentlogin(username, password):
                usertoken = tools.getsecretstr(tools.getnowtimestr()+password, username)
                return jsonify(logiclayer.updatestudenttoken(username, usertoken))
            else:
                return jsonify(Info(False, "用户名或密码错误").todict())
        else:
            return jsonify(Info(False, "数据库异常").todict())
    else:
        return jsonify(Info(False, "当前IP已有其他用户登录，请不要在同一电脑同时登录两个账户").todict())


@app.route("/studentregister", methods=["GET", "POST"])
def studentregister():
    if request.method == "GET":
        return render_template('studentregister.html')
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return jsonify(logiclayer.studentregitster(username, password))


@app.route("/problem_picpath", methods=["POST"])
def problem_picpath():
    try:
        lastproblem_id = logiclayer.getlastproblemid()
        newproblem_id = lastproblem_id + 1
        file = request.files["problem_picpath"]
        if file:
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid1()) + "." + filename.split(".")[-1]
            file.save(os.path.join(os.getcwd() + "/static/uploads/", filename))
            return render_template('addproblems.html', problem_id=newproblem_id,
                                   problem_filename=filename, problem_info="上传成功！")
    except Exception as e:
        filename = ""
        return render_template('addproblems.html', problem_id=newproblem_id,
                               problem_filename=filename, problem_info="上传失败！" + str(e))


@app.route("/addproblems", methods=["GET", "POST"])
def addproblems():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        if request.method == "GET":
            lastproblem_id = logiclayer.getlastproblemid()
            newproblem_id = lastproblem_id + 1
            return render_template('addproblems.html', problem_id=newproblem_id,
                                   problem_filename="",
                                   problem_info="请先选择文件再点击“开始上传”，只支持一张图片")
        elif request.method == "POST":
            problem_typestring = request.form["problem_typestring"].strip()
            problem_description = request.form["problem_description"].strip()
            problem_filename = request.form["problem_filename"].strip()
            problem_choiceA = request.form["problem_choiceA"].strip()
            problem_choiceB = request.form["problem_choiceB"].strip()
            problem_choiceC = request.form["problem_choiceC"].strip()
            problem_choiceD = request.form["problem_choiceD"].strip()
            problem_answer = request.form["problem_answer"].strip()
            return jsonify(logiclayer.addproblems(problem_typestring,
                                                  problem_description, problem_filename, problem_choiceA,
                                                  problem_choiceB, problem_choiceC, problem_choiceD,
                                                  problem_answer))
    else:
        return redirect("/adminlogin")


@app.route("/onlogin", methods=["POST"])
def onlogin():
    username = request.form["username"]
    password = request.form["password"]
    if logiclayer.checkadminlogin(username, password):
        return jsonify(Info(True, "登录成功").todict())
    else:
        return jsonify(Info(False, "用户名或密码错误").todict())


@app.route("/quitsystem", methods=["GET"])
def quitsystem():
    return render_template('index.html')


@app.route("/removeproblems", methods=["GET", "POST"])
def removeproblems():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        if request.method == "GET":
            return render_template('removeproblems.html')
        elif request.method == "POST":
            problem_id = request.form["problem_id"]
            return jsonify(logiclayer.removeproblems(problem_id))
    else:
        return redirect("/adminlogin")


@app.route("/grades", methods=["GET", "POST"])
def grades():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        if request.method == "GET":
            gradelist = logiclayer.getgradelist()
            return render_template('grades.html')
        elif request.method == "POST":
            return jsonify(logiclayer.getgradelist())
    else:
        return redirect("/adminlogin")


@app.route("/initstudents", methods=["GET"])
def initstudents():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        return render_template('initstudents.html')
    else:
        return redirect("/adminlogin")


@app.route("/modifypassword", methods=["GET", "POST"])
def modifypassword():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        if request.method == "GET":
            return render_template('modifypassword.html')
        elif request.method == "POST":
            oldpassword = request.form["oldpassword"]
            newpassword = request.form["newpassword"]
            username = request.cookies.get("username")
            return jsonify(logiclayer.modifypassword(oldpassword, newpassword, username))
    else:
        return redirect("/adminlogin")


@app.route("/importproblems", methods=["GET", "POST"])
def importproblems():
    username = request.cookies.get("username")
    if len(username.strip()) > 0:
        if request.method == "GET":
            return render_template('importproblems.html', problem_info="请先选择文件再点击“开始上传”")
        elif request.method == "POST":
            try:
                file = request.files["problemzip"]
                if file:
                    filename = secure_filename(file.filename)
                    filename = str(uuid.uuid1()) + "." + \
                        filename.split(".")[-1]
                    filepath = os.path.join(
                        os.getcwd() + "/static/uploads/", filename)
                    file.save(filepath)
                    flag = logiclayer.extractfile(filepath)
                    return render_template('importproblems.html', problem_info=flag["infomsg"])
            except Exception as e:
                print(e)
                return render_template('importproblems.html', problem_info="上传失败！"+str(e))
    else:
        return redirect("/adminlogin")


if __name__ == '__main__':
    if not os.path.exists(os.getcwd() + "/static/uploads/"):
        os.mkdir(os.getcwd() + "/static/uploads/")
    from gevent import pywsgi
    print("Server started at: http://"+str(conf.host)+":"+str(conf.port))
    server = pywsgi.WSGIServer( (conf.host, conf.port), app)
    server.serve_forever()

    # app.debug = True
    # app.run(host=conf.host, port=conf.port)
