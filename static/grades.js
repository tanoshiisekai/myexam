window.onload = function () {
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            if (result["infostatus"]) {
                var table = document.createElement("table");
                table.id = "aimtable";
                var th = table.insertRow();
                var thd;
                thd = th.insertCell();
                thd.innerHTML = "序号";
                thd = th.insertCell();
                thd.innerHTML = "用户名";
                thd = th.insertCell();
                thd.innerHTML = "答对题目的总数";
                thd = th.insertCell();
                thd.innerHTML = "答错题目的总数";
                thd = th.insertCell();
                thd.innerHTML = "答题用时";
                var tr, td;
                for (i in result["infodata"]["gradelist"]) {
                    tr = table.insertRow();
                    td = tr.insertCell();
                    td.innerHTML = parseInt(i) + 1;
                    td = tr.insertCell();
                    td.innerHTML = result["infodata"]["gradelist"][i]["user_username"];
                    td = tr.insertCell();
                    td.innerHTML = result["infodata"]["gradelist"][i]["userlog_right"];
                    td = tr.insertCell();
                    td.innerHTML = result["infodata"]["gradelist"][i]["userlog_wrong"];
                    td = tr.insertCell();
                    td.innerHTML = result["infodata"]["gradelist"][i]["userlog_timeduring"];
                }
                document.getElementById("gradetable").appendChild(table);
            } else {
                alert(result["infomsg"]);
            }
        }
    }
    xmlhttp.open("POST", baseurl + "/grades", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send();
}