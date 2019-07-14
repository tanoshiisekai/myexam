window.onload = function(){
    setcookie("username", "");
    document.getElementById("username").focus();
}

function keylogin(){
    if(event.keyCode==13){
        studentregister();
    }
}

function studentregister(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var repassword = document.getElementById("repassword").value;
    if(password != repassword){
        alert("新密码和确认密码不一致！请重新输入……");
        document.getElementById("password").value = "";
        document.getElementById("repassword").value = "";
    }else{
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
                    window.location.href=baseurl+"/";
                }else{
                    document.getElementById("username").value = "";
                }
            }
        }
        xmlhttp.open("POST", baseurl+"/studentregister",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send(jsontopost({"username": username, "password": password}));
    }
}

function studentlogin(){
    window.location.href=baseurl+"/";
}