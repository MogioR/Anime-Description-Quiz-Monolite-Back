var button_lc = document.getElementById("create-lobby");
button_lc.addEventListener("click", create_lobby);
var button_lc = document.getElementById("start-game");
button_lc.addEventListener("click", start_game);

function create_lobby() {
    socket.send(JSON.stringify({type: "lobby", action: "create"}));
}

function connect_lobby() {
    $("#lobby-sercher-menu").addClass("hide");
    $("#lobby-list").addClass("hide");
    $("#lobby").removeClass("hide");
    $("#lobby-menu").removeClass("hide");
}

function start_game() {
    socket.send(JSON.stringify({type: "lobby", action: "start"}));
    gameStart();
}

function updateLobbyPlayerList(event)
{
    var conteiner = document.querySelector('#lobby-player-conteiner');
    conteiner.innerHTML = '';
    console.log(event.players.length);
    for (let i = 0; i < event.players.length; i++)
    {
        console.log(event.players[i]);
        addPlayer(event.players[i]);
    }
}

function updateLobby(event) {
    for (let i = 0; i < event.lobbyes.length; i++)
        addLobby(event.lobbyes[i]);
}

function addLobby(lobby)
{
    var conteiner = document.querySelector('#lobby-conteiner');

    var newLobby =      document.createElement('div');
    var cont =          document.createElement('div');
    var hostName =      document.createElement('div');
    var hostName_d =     document.createElement('div');
    var hostNameSpan =  document.createElement('span');
    var occupancy =     document.createElement('div');
    var occupancy_d =     document.createElement('div');
    var occupancySpan =  document.createElement('span');
    var button_el =     document.createElement('div');
    var button_se =     document.createElement('div');
    var button_te =     document.createElement('div');
    var button =        document.createElement('button');
    button.innerText = 'Подключиться';
    button.addEventListener('click', () => {
        socket.send(JSON.stringify({type: "lobby", action: "connect", id: lobby.id}));
    })

    newLobby.className = 'lobby_element';
    cont.className = 'container clearfix';
    hostName.className = 'element middle_text';
    hostNameSpan.className = 'login_text text-upper';
    hostNameSpan.innerText = lobby.host;
    occupancy.className = 'element middle_text';
    occupancySpan.className = 'login_text text-upper';
    occupancySpan.innerText = "" + lobby.occupancy + '/' + lobby.size;
    button_el.className = 'element';
    button_se.className = 'stretch-element';
    button_te.className = 'table-cell';
    button.className = 'login_text text-upper';

    button_te.appendChild(button);
    button_se.appendChild(button_te);
    button_el.appendChild(button_se);

    hostName.appendChild(hostNameSpan);
    occupancy.appendChild(occupancySpan);

    cont.appendChild(hostName);
    cont.appendChild(occupancy);
    cont.appendChild(button_el);

    newLobby.appendChild(cont);
    conteiner.appendChild(newLobby);
}

function addPlayer(player_name)
{
    var conteiner = document.querySelector('#lobby-player-conteiner');
    var player =      document.createElement('div');
    var player_span = document.createElement('span');

    player.className = 'lobby_element middle_text';
    player_span.className = 'login_text text-upper';
    player_span.innerText = player_name;

    player.appendChild(player_span);
    conteiner.appendChild(player);
}
