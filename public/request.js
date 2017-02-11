var ws;

function doLoad() {
    ws = new WebSocket("ws://127.0.0.1:50007");
    ws.onmessage = function (evt) {
		console.log(evt)
        console.log(evt.data);
    }
}