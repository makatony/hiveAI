var ws;
var hexagons = [];
var slider;
var players = [];
var pieceColors = ['#00FF00', '#FFFF00'];

function setup() {
	createCanvas(600,500);
	textAlign(CENTER);
	
    ws = new WebSocket("ws://127.0.0.1:50007");
    ws.onmessage = function (evt) {
		webSocketListener(evt);
    }
	
	slider = createSlider(0,100,30);
	slider.position(10,10);
	
	setHexSize(30);
	
	
	createButton("getBoardPieces from server").mousePressed(function () {
		ws.send(JSON.stringify({
			action: "getBoardPieces"
		}));
	});
	
	var initBoardLayout = {
		"action": "setBoardLayout",
		"myPieces": [
			[-1,-1],
			[2,0],
			[3,0],
			[-2,-1],
			[-3,-1],
			[-1,1],
			[-2,1]
		],
		"oppPieces": [
			[0,0],
			[0,-1],
			[1,-1],
			[1,0],
			[0,1],
			[-1,0]
		]
	};
	
	myPlayer = new Player(0);
	oppPlayer = new Player(1);
	myPlayer.setPieces(initBoardLayout.myPieces);
	oppPlayer.setPieces(initBoardLayout.oppPieces);
	players.push(myPlayer);
	players.push(oppPlayer);
}


function draw() {
	background(0);
	setHexSize(slider.value());
	for (var j = 0; j < players.length; j++) {
		players[j].drawPieces();
	}
}

function Hexagon(gridPos) {
	this.gridPos = gridPos || createVector(0,0);
	this.pos = translateGrid2Pos(this.gridPos);
	this.caption = "";
	
	this.draw = function (color) {
		var col = color || 0;
		// push();
		// translate(this.pos);
		// rotate(frameCount / -100.0);
		push();
		fill(col);
		polygon(this.pos.x, this.pos.y, hexSize, 6);
		pop();
		push();
		fill(0);
		text(this.caption, this.pos.x, this.pos.y);
		pop();
	}
	
	this.setPos = function(position) {
		this.pos = position || createVector(width*0.5, height*0.5);
	}
	
	this.setCaption = function (cap) {
		this.caption = cap;
	}
	
	this.updatePos = function () {
		this.pos = translateGrid2Pos(this.gridPos);
	}
}

function Player(id) {
	this.pieces = [];
	this.hexagons = [];
	this.id = id || 0;

	this.setPieces = function(pieces_a) {
		if (pieces_a instanceof Array) {
			this.pieces = pieces_a;
			this.hexagons = [];
		}
		
		for (var i = 0; i < this.pieces.length; i++) {
			var thisHex = new Hexagon(createVector(this.pieces[i][0],this.pieces[i][1]));
			thisHex.updatePos();
			thisHex.setCaption(i+"/"+this.pieces[i][0]+","+this.pieces[i][1]);
			this.hexagons.push(thisHex);
		}
	}
	
	this.drawPieces = function () {
		for (var i = 0; i < this.hexagons.length; i++) {
			this.hexagons[i].updatePos();
			this.hexagons[i].draw(pieceColors[this.id]);
		}
	}
}







function translateGrid2Pos(grid) {
	var xPos = grid.x*hexHoffset;
	xPos = xPos + width/2;
	var yPos = grid.y * hexHeight;
	yPos = yPos + Math.abs(grid.x%2) * hexVoffset; //adding or not adding vertical offset
	yPos = yPos + height/2;
	return createVector(xPos,yPos);
}

// var hexSize = 30;
// var hexWidth = hexSize * 2;
// var hexHeight = Math.sqrt(3)/2 * hexWidth;
// var hexHoffset = hexWidth*3/4;
// var hexVoffset = hexHeight/2;


function polygon(x, y, radius, npoints) {
  var angle = TWO_PI / npoints;
  beginShape();
  for (var a = 0; a < TWO_PI; a += angle) {
    var sx = x + cos(a) * radius;
    var sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

function setHexSize(size){
	hexSize = size;
	hexWidth = hexSize * 2;
	hexHeight = Math.sqrt(3)/2 * hexWidth;
	hexHoffset = hexWidth*3/4;
	hexVoffset = hexHeight/2;
}


function mouseWheel(event) {
  slider.value(slider.value()+event.delta/20)
  return false;
}


function webSocketListener(evt) {
	json = JSON.parse(evt.data);
	if (json.action == "setBoardPieces") {
		if (players[0].id == 0) { // lots of assumptions here. works only for 2 players
			players[0].setPieces(json.myPieces);
			players[1].setPieces(json.oppPieces);
		}
		else {
			players[1].setPieces(json.myPieces);
			players[0].setPieces(json.oppPieces);
		}
	}
}
