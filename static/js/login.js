function validateForm() {
    var x = document.forms["Form"]["username"].value;
    if (x == "") {
        alert("请填写用户名！");
        return false;
    }
    var y = document.forms["Form"]["password"].value;
    if (y == "") {
        alert("密码为空！");
        return false;
    }
}
