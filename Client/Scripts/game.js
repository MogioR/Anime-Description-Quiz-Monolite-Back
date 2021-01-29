var gameSearchInput = document.getElementById("gameSearchInput");
gameSearchInput.addEventListener("input", () => {
   socket.send(JSON.stringify({type: "game", action: "reqestHints", data: gameSearchInput.value}));
});

var _1 = document.getElementById("req1");
_1.addEventListener("click", () =>{
    $("#req2").removeClass("select");
    $("#req3").removeClass("select");
    $("#req4").removeClass("select");
    $("#req1").addClass("select");
});

var _2 = document.getElementById("req2");
_2.addEventListener("click", () =>{
    $("#req1").removeClass("select");
    $("#req3").removeClass("select");
    $("#req4").removeClass("select");
    $("#req2").addClass("select");
});


var _3 = document.getElementById("req3");
_3.addEventListener("click", () =>{
    $("#req2").removeClass("select");
    $("#req1").removeClass("select");
    $("#req4").removeClass("select");
    $("#req3").addClass("select");
});

var _4 = document.getElementById("req4");
_4.addEventListener("click", () =>{
    $("#req2").removeClass("select");
    $("#req3").removeClass("select");
    $("#req1").removeClass("select");
    $("#req4").addClass("select");
});

function newAnswer(event)
{
    alert(event.discription);

    $("#discription-box").text(event.discription);

    $("#req1").removeClass("false");
    $("#req2").removeClass("false");
    $("#req3").removeClass("false");
    $("#req4").removeClass("false");
    $("#req1").removeClass("true");
    $("#req2").removeClass("true");
    $("#req3").removeClass("true");
    $("#req4").removeClass("true");
    $("#req1").val(event.answers[0]);
    $("#req2").val(event.answers[1]);
    $("#req3").val(event.answers[2]);
    $("#req4").val(event.answers[3]);


    //let fruits = ["Яблоко", "Апельсин", "Слива"];
    //updateSearchSelector("answerSearchSelector", fruits);
}

function trueAnswer(event)
{
    $("#req1").removeClass("select");
    $("#req2").removeClass("select");
    $("#req3").removeClass("select");
    $("#req4").removeClass("select");
    $("#req1").addClass("false");
    $("#req2").addClass("false");
    $("#req3").addClass("false");
    $("#req4").addClass("false");
    $("#req"+(event.trueAnswer+1)).removeClass("false");
    $("#req"+(event.trueAnswer+1)).addClass("true");
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

