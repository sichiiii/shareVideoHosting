var client_id = Date.now()
var player;

// this function gets called when API is ready to use
function onYouTubePlayerAPIReady() {
  // create the global player from the specific iframe (#video)
  player = new YT.Player("video", {
    events: {
      // call this function when player is ready to use
      onReady: onPlayerReady
    }
  });
}
function onPlayerReady(event) {
  event.target.setVolume(100);
  event.target.playVideo();
}

var tag = document.createElement("script");
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
    var input = document.getElementById("messageText")
    var ul = document.getElementById("messages");
    var mango = ul.children[ul.children.length - 1];
    var status = mango.textContent
    if (status.slice(-4) == 'play'){
        player.playVideo();
      }
    if (status.slice(-4) == 'stop'){
        player.pauseVideo();
        let seconds = player.getCurrentTime();
      }
  function checkTime() {
      if (player.currentTime >= seconds) {
        player.pauseVideo();
      } else {
        setTimeout(checkTime, 100);
      }
  }
  checkTime()
};
function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
function sendPause(event) {
    ws.send('stop')
    event.preventDefault()
    var pauseButton = document.getElementById("pause-button");
    pauseButton.addEventListener("click", function () {
      player.pauseVideo();
    });
}
function sendStart(event) {
    var playButton = document.getElementById("play-button");
    playButton.addEventListener("click", function () {
    player.playVideo();
    });
    ws.send('play')
    event.preventDefault()
}