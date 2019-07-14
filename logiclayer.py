import conf
from dbtools import db, User, Admin, Problem, UserLog
from sqlalchemy import and_
from info import Info
import zipfile
import os
import uuid
from pyexcel_xls import get_data as get_data_xls
from pyexcel_xlsx import get_data as get_data_xlsx
import shutil
import random
from flask import url_for
import hashlib
import string
import tools


def checkusertoken(username, token):
    tk = db.session.query(User).filter(
        and_(
            User.user_username == username,
            User.user_token == token
        )
    ).first()
    if tk:
        return True
    else:
        return False


def getproblembyid(idstr):
    problem = db.session.query(Problem).filter(
        Problem.problem_id == idstr).first()
    if problem:
        problem_id = problem.problem_id
        problem_typestring = problem.problem_typestring
        problem_description = problem.problem_description
        if len(problem.problem_picpath.strip()) == 0:
            hasimage = False
        else:
            hasimage = True
        problem_picpath = url_for(
            'static', filename="uploads/"+problem.problem_picpath, _external=True)
        problem_choiceA = problem.problem_choiceA
        problem_choiceB = problem.problem_choiceB
        problem_choiceC = problem.problem_choiceC
        problem_choiceD = problem.problem_choiceD
        key = tools.getrandomanswer()
        problem_answer = tools.getsecretstr(problem.problem_answer, key)
        return Info(True, "题目获取成功", {"problem_id": problem_id,
                                     "problem_typestring": problem_typestring,
                                     "problem_description": problem_description,
                                     "problem_picpath": problem_picpath,
                                     "problem_choiceA": problem_choiceA,
                                     "problem_choiceB": problem_choiceB,
                                     "problem_choiceC": problem_choiceC,
                                     "problem_choiceD": problem_choiceD,
                                     "problem_answer": problem_answer,
                                     "important_key": key,
                                     "hasimage": hasimage}).todict()
    else:
        return Info(False, "题目获取失败，查询不到的题目").todict()


def getrandomproblemlist():
    ids = db.session.query(Problem.problem_id).all()
    if ids:
        ids = [x[0] for x in ids]
        random.shuffle(ids)
        ids = ids[:conf.totalproblems]
    else:
        ids = []
    return ids


def getlastproblemid():
    ad = db.session.query(Problem).order_by(Problem.problem_id.desc()).first()
    if ad:
        return int(ad.problem_id)
    else:
        return 0


def checkstudentlogin(username, password):
    ad = db.session.query(User).filter(
        and_(
            User.user_username == username,
            User.user_password == password
        )
    ).first()
    if ad:
        return True
    return False


def checkadminlogin(username, password):
    ad = db.session.query(Admin).filter(
        and_(
            Admin.admin_username == username,
            Admin.admin_password == password
        )
    ).first()
    if ad:
        return True
    return False


def modifypassword(oldpassword, newpassword, username):
    ad = db.session.query(Admin).filter(
        and_(
            Admin.admin_username == username,
            Admin.admin_password == oldpassword
        )
    ).first()
    if not ad:
        return Info(False, "原密码错误！").todict()
    else:
        db.session.query(Admin).filter(Admin.admin_username == username).update(
            {"admin_password": newpassword})
        db.session.commit()
        return Info(True, "密码修改成功！").todict()


def removestudentip(username, remoteip):
    try:
        db.session.query(User).filter(
            and_(User.user_username == username, User.user_ip == remoteip)).update(
            {"user_ip": ""})
        db.session.commit()
    except Exception as e:
        return False
    else:
        return True


def checkstudentip(username, remoteip):
    user = db.session.query(User).filter(User.user_ip == remoteip).first()
    if user:
        if user.user_username == username:
            return True
        else:
            return False
    else:
        return True


def updatestudentip(username, remoteip):
    try:
        db.session.query(User).filter(User.user_username == username).update(
            {"user_ip": remoteip})
        db.session.commit()
    except Exception as e:
        return False
    else:
        return True


def updatestudenttoken(username, usertoken):
    db.session.query(User).filter(User.user_username == username).update(
        {"user_token": usertoken})
    db.session.commit()
    return Info(True, "登录成功", usertoken).todict()


def studentregitster(username, password):
    us = db.session.query(User).filter(
        User.user_username == username,
    ).first()
    if us:
        return Info(False, "已存在的用户名！").todict()
    else:
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return Info(True, "注册成功！").todict()


def removeproblems(problem_id):
    pr = db.session.query(Problem).filter(
        Problem.problem_id == problem_id
    ).first()
    if pr:
        db.session.delete(pr)
        db.session.commit()
        return Info(True, "删除成功！").todict()
    else:
        return Info(False, "不存在的题号！").todict()


def addproblems(problem_typestring, problem_description, problem_picpath,
                problem_choiceA, problem_choiceB, problem_choiceC, problem_choiceD,
                problem_answer):
    pr = db.session.query(Problem).filter(
        and_(
            Problem.problem_description == problem_description,
            Problem.problem_choiceA == problem_choiceA,
            Problem.problem_choiceB == problem_choiceB,
            Problem.problem_choiceC == problem_choiceC,
            Problem.problem_choiceD == problem_choiceD,
            Problem.problem_answer == problem_answer
        )
    ).first()
    if pr:
        return Info(False, "已存在的题目！如果确定不是重复的题目，请修改题目中的信息后重新提交。").todict()
    else:
        problem = Problem(problem_typestring, problem_description, problem_picpath,
                          problem_choiceA, problem_choiceB, problem_choiceC, problem_choiceD,
                          problem_answer)
        db.session.add(problem)
        db.session.commit()
        return Info(True, "提交成功！").todict()


def extractfile(filepath):
    # 解压缩
    uploaddir = os.path.split(filepath)[0]
    file_zip = zipfile.ZipFile(filepath, "r")
    tempdirname = file_zip.filename.replace(".zip", "")
    os.mkdir(tempdirname)
    for f in file_zip.namelist():
        file_zip.extract(f, tempdirname)
    file_zip.close()
    os.remove(filepath)
    # 解析
    tablefilepath = os.path.join(tempdirname, conf.defaulttablefilename)
    picdir = os.path.join(tempdirname, conf.defaultpicfiledir)
    if tablefilepath.endswith(".xls"):
        data = get_data_xls(tablefilepath)[conf.defaulttablefilesheet][1:]
    elif tablefilepath.endswith(".xlsx"):
        data = get_data_xlsx(tablefilepath)[conf.defaulttablefilesheet][1:]
    allcount = 0
    passcount = 0
    failcount = 0
    for dt in data:
        problem_typestring = dt[1]
        problem_description = dt[2]
        problem_choiceA = dt[3]
        problem_choiceB = dt[4]
        problem_choiceC = dt[5]
        problem_choiceD = dt[6]
        problem_answer = dt[7]
        if len(dt) > 8:
            newpicname = str(uuid.uuid1()) + "." + dt[8].split(".")[-1]
            shutil.move(os.path.join(tempdirname + "/" + conf.defaultpicfiledir,
                                     dt[8]), os.path.join(uploaddir, newpicname))
            problem_picpath = newpicname
        else:
            problem_picpath = ""
        ap = addproblems(problem_typestring, problem_description, problem_picpath,
                         problem_choiceA, problem_choiceB, problem_choiceC, problem_choiceD,
                         problem_answer)
        allcount = allcount + 1
        if ap["infostatus"] == True:
            passcount = passcount + 1
        else:
            print(ap["infomsg"])
            failcount = failcount + 1
    shutil.rmtree(tempdirname)
    return Info(True, str(passcount)+"条数据导入成功，"+str(failcount)+"条数据导入失败，共"+str(allcount)+"条数据。").todict()


def updateuser(username, userright, userwrong, usertimeduring, userchoicelog):
    userid = db.session.query(User.user_id).filter(
        User.user_username == username).first()
    if userid:
        userid = userid[0]
        lastlog = db.session.query(UserLog).filter(
            and_(
                UserLog.userlog_userid == userid,
                UserLog.userlog_status == 0
            )
        ).first()
        if lastlog:
            db.session.query(UserLog).filter(
                UserLog.userlog_userid == userid,
            ).update({"userlog_status": 1})
        userlog_userid = userid
        userlog_right = userright
        userlog_wrong = userwrong
        userlog_timeduring = usertimeduring
        userlog_status = 0
        userlog_choicelog = userchoicelog
        ul = UserLog(userlog_userid, userlog_right, userlog_wrong,
                     userlog_timeduring, userlog_status, userlog_choicelog)
        try:
            db.session.add(ul)
            db.session.commit()
        except Exception as e:
            print(e)
            return Info(False, "考试数据提交失败，请联系系统管理员！（"+str(userlog_choicelog)+"）").todict()
        else:
            return Info(True, "考试数据提交成功", {"userlog_timeduring": userlog_timeduring}).todict()
    else:
        return Info(False, "非法的用户名").todict()


def initstudents():
    try:
        db.session.query(UserLog).update({"userlog_status": 1})
        db.session.commit()
    except Exception as e:
        print(e)
        return Info(False, "初始化失败！"+str(e)).todict()
    else:
        return Info(True, "初始化成功！").todict()


def getgradelist():
    loglist = db.session.query(User, UserLog).join(
        User, UserLog.userlog_userid == User.user_id
    ).filter(
        UserLog.userlog_status == 0
    ).all()
    templist = []
    resultlist = []
    for lg in loglist:
        username = str(lg[0].user_username)
        userright = str(lg[1].userlog_right)
        userwrong = str(lg[1].userlog_wrong)
        usertimeduring = str(lg[1].userlog_timeduring)
        templist.append([username, userright, userwrong, usertimeduring])
    templist.sort(key=lambda x:(int(x[1]), -int(x[3])), reverse=True)
    for tp in templist:
        resultlist.append({"user_username": tp[0],
                           "userlog_right": tp[1],
                           "userlog_wrong": tp[2],
                           "userlog_timeduring": tp[3]})
    if loglist:
        return Info(True, "成绩查询成功", {
            "gradelist": resultlist
        }).todict()
    else:
        return Info(False, "没有考生信息").todict()
