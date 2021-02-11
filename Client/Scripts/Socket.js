var socket = new WebSocket("ws://127.0.0.1:5678/");

socket.onmessage = function(e) {
    console.log(e.data)
    let event = JSON.parse(e.data);

    if(event.type == "login")
    {
        loginEvent(event);
    }
    else if(event.type == "lobbyList")
    {
        updateLobby(event);
    }
    else if(event.type == "lobby")
    {
        if(event.action == "enter")
            connect_lobby();
        else if(event.action == "getPlayerList")
            updateLobbyPlayerList(event);
        else if(event.action == "startGame")
            gameStart();
    }
    else if(event.type == "game")
    {
        if(event.action == "trueAnswer")
            trueAnswer(event);
        else if(event.action == "newAnswer")
            newAnswer(event);
        else if(event.action == "newHints")
            updateSearchSelector("answerSearchSelector", event.hints);
    }
};

socket.onopen = function() {
  console.log("Соединение установлено.");
};

/*
socket.onclose = function(event) {
  if (event.wasClean) {
    alert('Соединение закрыто чисто');
  } else {
    alert('Обрыв соединения'); // например, "убит" процесс сервера
  }
  alert('Код: ' + event.code + ' причина: ' + event.reason);
};



socket.onerror = function(error) {
  alert("Ошибка " + error.message);
};
*/