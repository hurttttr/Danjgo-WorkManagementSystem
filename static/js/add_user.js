function validateForm() {
    var x = document.forms["Form"]["password"].value;
    var y = document.forms["Form"]["passwordagain"].value;
    if (x != y) {
        alert("两次密码不一致！");
        return false;
    }
    if (x.length < 6) {
        alert("密码长度不能小于6！");
        return false;
    }
}
