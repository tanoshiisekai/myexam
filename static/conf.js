serverip = "192.168.2.110"
serverport = "8080"
baseurl = "http://" + serverip + ":" + serverport

maxtime = 60

var xmlhttp;
if (window.XMLHttpRequest) {
    //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp = new XMLHttpRequest();
}
else {
    // IE6, IE5 浏览器执行代码
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}


function jsontopost(value) {
    var pstr = "";
    for (var key in value) {
        pstr += key + "=" + encodeURI(value[key]) + "&";
    };
    return pstr;
}

function setcookie(cname, cvalue, exdays) {
    var d = new Date();
    if (!exdays) {
        exdays = 1;
    }
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getcookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

String.prototype.endwith=function(endStr){
    var d=this.length-endStr.length;
    return (d>=0&&this.lastIndexOf(endStr)==d);
}

function getnowtime(){
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    return year + "_" + month + "_" + day + "_" + hour + "_" + minute + "_" + second;
}

function getmd5str(aimstr, key){
    var hash = md5.create();
    hash.update(aimstr + key);
    return hash.hex();
}
