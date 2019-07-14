window.onload = function () {
    var n = maxtime;
    auto = window.setInterval(function(){
        countdown(n);
    }, 1000);
    document.getElementById("token").value = getcookie("token");
    // auto = window.setInterval("countdown()", 1000);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            ids = result["infodata"]["problemlist"];
            if (result["infostatus"]) {
                document.getElementById("problemlist").value = ids;
                document.getElementById("totalcount").value = ids.length;
                document.getElementById("rightcount").value = 0;
            }
        }
    }
    xmlhttp.open("GET", baseurl + "/getproblemsid", true);
    xmlhttp.send();
}


function logout() {
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
            if (result["infostatus"]) {
                setcookie("username", "");
                window.location.href = "/";
            }
        }
    }
    xmlhttp.open("GET", baseurl + "/removeip", true);
    xmlhttp.send();
}


function strtoarray(str) {
    return str.split(",");
}


function finished(){
    var user_right = document.getElementById("rcount").innerHTML;
    var user_wrong = document.getElementById("fcount").innerHTML;
    var timestart = document.getElementById("starttime").value;
    var timeend = document.getElementById("endtime").value;
    var userchoicelog = document.getElementById("userchoicelog").value;
    var secret = getmd5str(user_right+user_wrong+timestart+timeend+userchoicelog,timeend);
    var token = document.getElementById("token").value;
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            if(result["infostatus"]){
                document.getElementById("userlog_timeduring").innerHTML = result["infodata"]["userlog_timeduring"];
            }else{
                alert(result["infomsg"]);
            }
        }
    }
    xmlhttp.open("POST", baseurl + "/finished", true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(jsontopost({
        "user_right": user_right,
        "user_wrong": user_wrong,
        "timestart": timestart,
        "timeend": timeend,
        "userchoicelog": userchoicelog,
        "secret": secret,
        "token": token
    }));
}

function nextproblem() {
    document.getElementById("totalnumber").innerHTML = document.getElementById("totalcount").value;
    var pnumber = parseInt(document.getElementById("problemnumber").innerHTML);
    pnumber = pnumber + 1;
    document.getElementById("problemnumber").innerHTML = pnumber;
    document.getElementById("remain").innerHTML = maxtime;
    var pid = document.getElementById("problemid").value;
    var useranswer = document.getElementById("answerbox").value;
    var key = document.getElementById("answer").value;
    var userlog = document.getElementById("userchoicelog").value;
    userlog = userlog + pid + "_" + useranswer + "*";
    document.getElementById("userchoicelog").value = userlog;
    useranswer = getmd5str(useranswer, key);
    var systemanswer = document.getElementById("important_key").value;
    var rightcount = parseInt(document.getElementById("rightcount").value);
    if (useranswer == systemanswer) {
        rightcount = rightcount + 1;
        document.getElementById("rightcount").value = rightcount;
    }
    var ids = strtoarray(document.getElementById("problemlist").value);
    var currentid = ids.shift();
    document.getElementById("problemlist").value = ids;
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            if (result["infostatus"]) {
                problem = result["infodata"];
                console.log(problem);
                document.getElementById("problemid").value = problem["problem_id"];
                document.getElementById("typestring").innerHTML = problem["problem_typestring"];
                document.getElementById("description").innerHTML = problem["problem_description"];
                if (problem["hasimage"]) {
                    document.getElementById("picpath").src = problem["problem_picpath"];
                    document.getElementById("picpath").style = "display:block;";
                } else {
                    document.getElementById("picpath").style = "display:none;";
                }
                document.getElementById("choiceA").innerHTML = "A: " + problem["problem_choiceA"];
                document.getElementById("choiceB").innerHTML = "B: " + problem["problem_choiceB"];
                document.getElementById("choiceC").innerHTML = "C: " + problem["problem_choiceC"];
                document.getElementById("choiceD").innerHTML = "D: " + problem["problem_choiceD"];
                document.getElementById("important_key").value = problem["problem_answer"];
                document.getElementById("answerline").style = "display:block;";
                document.getElementById("timebox").style = "display:block;";
                document.getElementById("answerbox").value = "";
                document.getElementById("answer").value = problem["important_key"];
            } else {
                clearInterval(auto);
                document.getElementById("endtime").value = getnowtime();
                document.getElementById("content").style = "display:none;";
                document.getElementById("content1").style = "display:block";
                var totalcount = document.getElementById("totalcount").value;
                var rightcount = document.getElementById("rightcount").value;
                document.getElementById("tcount").innerHTML = totalcount;
                document.getElementById("rcount").innerHTML = rightcount;
                var failcount = parseInt(totalcount) - parseInt(rightcount);
                document.getElementById("fcount").innerHTML = failcount;
                // 答题结果发送到服务端
                finished();
            }
        }
    }
    xmlhttp.open("GET", baseurl + "/getproblembyid?problemid=" + currentid, true);
    xmlhttp.send();
}


function countdown(ntime) {
    try{
        var timeremain = parseInt(document.getElementById("remain").innerHTML);
    }catch(e){
        alert("计时器被篡改，请重新答题。");
        window.location.href="/";
    }
    timeremain = timeremain - 1;
    if(timeremain > ntime){
        alert("计时器被篡改，请重新答题。");
        window.location.href="/";
    }
    document.getElementById("remain").innerHTML = timeremain;
    if (timeremain == 0) {
        nextproblem();
    }
}


function startexam() {
    document.getElementById("starttime").value = getnowtime();
    document.getElementById("endtime").value = "";
    document.getElementById("totalnumber").innerHTML = document.getElementById("totalcount").value;
    document.getElementById("problemnumber").innerHTML = 1;
    document.getElementById("remain").innerHTML = maxtime;
    document.getElementById("startpanel").style = "display:none;";
    var ids = strtoarray(document.getElementById("problemlist").value);
    var currentid = ids.shift();
    document.getElementById("problemlist").value = ids;
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            if (result["infostatus"]) {
                problem = result["infodata"];
                console.log(problem);
                document.getElementById("problemid").value = problem["problem_id"];
                document.getElementById("typestring").innerHTML = problem["problem_typestring"];
                document.getElementById("description").innerHTML = problem["problem_description"];
                if (problem["hasimage"]) {
                    document.getElementById("picpath").src = problem["problem_picpath"];
                    document.getElementById("picpath").style = "display:block;";
                } else {
                    document.getElementById("picpath").style = "display:none;";
                }
                document.getElementById("choiceA").innerHTML = "A: " + problem["problem_choiceA"];
                document.getElementById("choiceB").innerHTML = "B: " + problem["problem_choiceB"];
                document.getElementById("choiceC").innerHTML = "C: " + problem["problem_choiceC"];
                document.getElementById("choiceD").innerHTML = "D: " + problem["problem_choiceD"];
                document.getElementById("important_key").value = problem["problem_answer"];
                document.getElementById("answer").value = problem["important_key"];
                document.getElementById("answerline").style = "display:block;";
                document.getElementById("timebox").style = "display:block;";
                document.getElementById("answerbox").value = "";
                document.getElementById("userchoicelog").value = "";
            } else {
                alert("题库中没有题目");
            }
        }
    }
    xmlhttp.open("GET", baseurl + "/getproblembyid?problemid=" + currentid, true);
    xmlhttp.send();
}
