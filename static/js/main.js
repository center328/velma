var ws = new WebSocket(location.href.replace('http', 'ws') + 'ws');

function initiatorCtrl(event) {
    console.log(event.data);
    if (event.data == "connected") {
        init();
    }
}

ws.onmessage = initiatorCtrl;

function init () {
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.onresult = function(event) {
      console.log(event['results'][0][0]['transcript']);
      console.log(event['results'][0][0]['confidence']);
      console.log(event['results'][0]['isFinal']);
    }
    recognition.start();
}



