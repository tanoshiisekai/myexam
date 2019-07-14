
function modifypassword(){
    var oldpassword = document.getElementById("oldpassword").value;
    var newpassword = document.getElementById("newpassword").value;
    var repassword = document.getElementById("repassword").value;
    if(newpassword != repassword){
        alert("新密码和确认密码不一致！请重新输入……");
        document.getElementById("newpassword").value = "";
        document.getElementById("repassword").value = "";
    }else{
        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
                var result = JSON.parse(xmlhttp.responseText);
                alert(result["infomsg"]);
                if (!result["infostatus"]){
                    document.getElementById("oldpassword").value = "";
                }else{
                    document.getElementById("newpassword").value = "";
                    document.getElementById("repassword").value = "";
                    document.getElementById("oldpassword").value = "";
                }
            }
        }
        xmlhttp.open("POST", baseurl+"/modifypassword",true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send(jsontopost({"oldpassword": oldpassword, "newpassword": newpassword}));
    }
}