var button1 = document.getElementById("login_button");
button1.addEventListener("click", updateButton);

function updateButton() {
   socket.send(JSON.stringify({type: "login", nickname: $("#login_box").val(), password: $("#pass_box").val()}));
}

function loginEvent(event) {
    if(event.login == 1)
    {
        $("#login-menu").addClass("hide");
        $("#loading-text").addClass("hide");
        $("#lobby-sercher-menu").removeClass("hide");
        $("#lobby-list").removeClass("hide");
    }
}