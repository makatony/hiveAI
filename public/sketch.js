var ws;
var hexagons = [];
var slider;
var boards = [];
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
	
	var boardPieces = [
        {
            "row": -1,"col": -1,"player": 0,"insect": "S"
        },
        {
            "row": 2,"col": 0,"player": 0,"insect": "A"
        },
        {
            "row": 3,"col": 0,"player": 0,"insect": "Q"
        },
        {
            "row": -2,"col": -1,"player": 0,"insect": "B"
        },
        {
            "row": -3,"col": -1,"player": 0,"insect": "A"
        },
        {
            "row": -1,"col": 1,"player": 0,"insect": "A"
        },
        {
            "row": -2,"col": 1,"player": 0,"insect": "A"
        },
        {
            "row": 0,"col": 0,"player": 1,"insect": "B"
        },
        {
            "row": 0,"col": -1,"player": 1,"insect": "G"
        },
        {
            "row": 1,"col": -1,"player": 1,"insect": "A"
        },
        {
            "row": 1,"col": 0,"player": 1,"insect": "A"
        },
        {
            "row": 0,"col": 1,"player": 1,"insect": "A"
        },
        {
            "row": -1,"col": 0,"player": 1,"insect": "Q"
        }
    ];
	
	var board = new Board();
	board.resetBoardPieces(boardPieces);
	boards.push(board);
	
	
	/*
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
	*/
}


function draw() {
	background(0);
	setHexSize(slider.value());
	
	boards[0].drawPieces(); //assuming we only have one board
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

function Board() { // [{"row": 0,"col": 1,"player": 0,"insect": "S"},{....}]
	this.pieces = [];
	
	this.resetBoardPieces = function(boardPieces_a) {
		this.pieces = [];
		for (var i = 0; i < boardPieces_a.length; i++) {
			var p = boardPieces_a[i];
			var thisPiece = new Piece(p.insect,p.col,p.row,p.player)
			thisPiece.setHexagon(thisPiece.gridPos);
			this.pieces.push(thisPiece);
		}
	}	
	
	this.drawPieces = function () {
		for (var i = 0; i < this.pieces.length; i++) {
			this.pieces[i].drawHexagon();
		}
	}
}

function Piece(insect,col,row,playerId) {
	this.insect = insect||'n/a';
	this.gridPos = createVector(col||0,row||0); // grid-position is a vector described in COLUMN and ROW
	this.playerId = playerId||0;	// 0 = me ; 1 = AI opponent
	
	this.setHexagon = function(gridPos) {
		this.hexagon = new Hexagon(gridPos);
		this.hexagon.updatePos(); // hexagon's pos is described in PIXELS. so the gridPos needs to be translated to pixels
		this.hexagon.setCaption(this.insect+" / "+this.gridPos.x+","+this.gridPos.y);
	}
	
	this.drawHexagon = function () {
		this.hexagon.updatePos();
		this.hexagon.draw(pieceColors[this.playerId]);
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
	// console.log(JSON.stringify(json,null,0))
	if (json.action == "setBoardPieces") {
		boards[0].resetBoardPieces(json.boardPieces); // ssuming only one board
		
		//TODO: there are pieces missing in boardPieces. in server.py the board.positions only shows the visible pieces, not the pieces under the beetles
		//as per Jan: board.covered is a dict of position -> list of pieces ; in order bottom-to-top piece ; only the very top piece is stored in board.positions
	}
}
