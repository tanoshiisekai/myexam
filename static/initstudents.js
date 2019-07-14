function initstudents(){
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
        }
    }
    xmlhttp.open("GET", baseurl + "/doinitstudents", true);
    xmlhttp.send();
}