window.onload = function(){
    setcookie("username", "");
    document.getElementById("username").focus();
}

function keylogin(){
    if(event.keyCode==13){
        studentlogin();
    }
}

function studentlogin(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var hash = md5.create();
    hash.update(password);
    password = hash.hex();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
            if(result["infostatus"]){
                setcookie("username", username);
                setcookie("token", result["infodata"]);
                window.location.href=baseurl+"/exam";
            }
        }
    }
    xmlhttp.open("POST", baseurl+"/studentlogin",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(jsontopost({"username": username, "password": password}));
}

function studentregister(){
    window.location.href=baseurl+"/studentregister";
}
