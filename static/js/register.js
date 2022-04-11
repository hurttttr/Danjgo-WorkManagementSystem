function validateForm() {
    var x = document.forms["Form"]["user"].value;
    if (x == "") {
        alert("请填写用户名！");
        return false;
    }
    var z = document.forms['Form']['name'].value;
    if (z == "") {
        alert("姓名为空！");
        return false;
    }
    var y = document.forms["Form"]["password"].value;
    if (y == "") {
        alert("密码为空！");
        return false;
    }
    if (y.length < 6) {
        alert("密码长度不能小于6！");
        return false;
    }
}
