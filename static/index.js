window.onload = function(){
    setcookie("username", "");
    document.getElementById("username").focus();
}

function keylogin(){
    if(event.keyCode==13){
        adminlogin();
    }
}

function adminlogin(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
            setcookie("username", username);
            if(result["infostatus"]){
                window.location.href=baseurl+"/addproblems";
            }
        }
    }
    xmlhttp.open("POST", baseurl+"/onlogin",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(jsontopost({"username": username, "password": password}));
}

