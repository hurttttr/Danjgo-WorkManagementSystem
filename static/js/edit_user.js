function validateForm() {
    var x = document.forms["Form"]["password"].value;
    var y = document.forms["Form"]["passwordagain"].value;
    if (x != y) {
        alert("两次密码不一致！");
        return false;
    }
}
