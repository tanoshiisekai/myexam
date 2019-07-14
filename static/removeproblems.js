function removeproblems(){
    var problem_id = document.getElementById("problem_id").value;
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
            if(result["infostatus"]){
                window.location.href=baseurl+"/removeproblems";
            }
        }
    }
    xmlhttp.open("POST", baseurl+"/removeproblems",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(jsontopost({
        "problem_id": problem_id,
    }));
}

