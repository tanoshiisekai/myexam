function addproblems(){
    var problem_typestring = document.getElementById("problem_typestring").value;
    var problem_description = document.getElementById("problem_description").value;
    var problem_filename = document.getElementById("problem_filename").value;
    var problem_choiceA = document.getElementById("problem_choiceA").value;
    var problem_choiceB = document.getElementById("problem_choiceB").value;
    var problem_choiceC = document.getElementById("problem_choiceC").value;
    var problem_choiceD = document.getElementById("problem_choiceD").value;
    var problem_answer = document.getElementById("problem_answer").value;
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var result = JSON.parse(xmlhttp.responseText);
            alert(result["infomsg"]);
            if(result["infostatus"]){
                window.location.href=baseurl+"/addproblems";
            }
        }
    }
    xmlhttp.open("POST", baseurl+"/addproblems",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(jsontopost({
        "problem_typestring": problem_typestring,
        "problem_description": problem_description,
        "problem_filename": problem_filename,
        "problem_choiceA": problem_choiceA,
        "problem_choiceB": problem_choiceB,
        "problem_choiceC": problem_choiceC,
        "problem_choiceD": problem_choiceD,
        "problem_answer": problem_answer
    }));
}

