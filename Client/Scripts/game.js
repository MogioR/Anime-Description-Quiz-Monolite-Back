var gameSearchInput = document.getElementById("gameSearchInput");
gameSearchInput.addEventListener("input", () => {
   socket.send(JSON.stringify({type: "game", action: "reqestHints", data: gameSearchInput.value}));
});

function newAnswer(event)
{

}

function trueAnswer(event)
{

}

function updateSearchSelector(selector, hints)
{
    var selector_box = document.querySelector("#" + selector);
    selector_box.innerHTML = '';

    if(hints.length != 0)
    {
        var option = document.createElement('option');
        option.innerText = hints[0];
        option.setAttribute('selected', true);
        selector_box.appendChild(option);
        for (let i = 1; i < hints.length; i++)
        {
            option = document.createElement('option');
            option.innerText = hints[i];
            selector_box.appendChild(option);
        }
    }
}

function submitAnswer()
{

}

function gameStart()
{
    $("#lobby").addClass("hide");
    $("#lobby-menu").addClass("hide");
    $("#game-menu").removeClass("hide");
    $("#game").removeClass("hide");
}

