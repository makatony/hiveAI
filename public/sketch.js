var ws;
var slider;
var boards = [];
var pieceColors = ['#00FF00', '#FFFF00'];
var draggingPiece;
var drawEmptyNeighbors;

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
            "row": -2,"col": 2,"player": 0,"insect": "A"
        },
        {
            "row": -1,"col": 2,"player": 0,"insect": "A"
        },
        {
            "row": -1,"col": 3,"player": 0,"insect": "A"
        },
        {
            "row": -2,"col": 3,"player": 0,"insect": "A"
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
        },
        {
            "row": -1,"col": -2,"player": 1,"insect": "Q"
        },
        {
            "row": -2,"col": -2,"player": 1,"insect": "Q"
        },
        {
            "row": -3,"col": -2,"player": 1,"insect": "Q"
        },
        {
            "row": -1,"col": -3,"player": 1,"insect": "Q"
        },
        {
            "row": -2,"col": -3,"player": 1,"insect": "Q"
        },
        {
            "row": -3,"col": -3,"player": 1,"insect": "Q"
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
	background(51);
	setHexSize(slider.value());
	
	if (drawEmptyNeighbors != undefined) drawDotOnGridPos(drawEmptyNeighbors);
	
	boards[0].drawPieces(); //assuming we only have one board
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
	
	this.neighbours = function (gridPos) {
		var x = gridPos.x;
		var y = gridPos.y;
        if (x % 2 == 0) return [createVector(x, y - 1), createVector(x + 1, y - 1), createVector(x + 1, y), createVector(x, y + 1), createVector(x - 1, y), createVector(x - 1, y - 1)]
        else 			return [createVector(x, y - 1), createVector(x + 1, y), createVector(x + 1, y + 1), createVector(x, y + 1), createVector(x - 1, y + 1), createVector(x - 1, y)]
	}
	
	this.isOccupied = function(gridPos) { // gridPos = p5.Vector
		for (var i = 0; i < this.pieces.length; i++) {
			if (gridPos.equals(this.pieces[i].gridPos)) return true;
		}
		return false;
	}
	
	this.emptyNeighbours = function(gridPos) {
		
	}
	
	this.allEmptyNeighbours = function(gridPos,visited) {
		if (visited == undefined) var visited = [];
		if (gridPos == undefined) var gridPos = createVector(0,0);
		var emptySlots = [];
		
		//checking if this node was visited already, if yes return empty array (break out of this recursion)
		for (var j = 0; j < visited.length; j++) if ((visited[j].x == gridPos.x) && (visited[j].y == gridPos.y)) return [];
		visited.push(gridPos);
		
		var neighbours_a = this.neighbours(gridPos);
		for (var i = 0; i < neighbours_a.length; i++) {
			if (this.isOccupied(neighbours_a[i])) 	emptySlots = emptySlots.concat(this.allEmptyNeighbours(neighbours_a[i],visited)); //branch node in recursion
			else 									emptySlots.push(neighbours_a[i]); //leaf node in recursion
		}
		
		return emptySlots;
	}
	
	this.validEmptyNeighbours = function(thisPlayer,gridPos,visited) {
		if (visited == undefined) var visited = [];
		if (gridPos == undefined) var gridPos = createVector(0,0);
		var emptySlots = [];
		var oppPlayer = 1-thisPlayer;
		
		//checking if this node was visited already, if yes return empty array (break out of this recursion)
		for (var j = 0; j < visited.length; j++) if ((visited[j].x == gridPos.x) && (visited[j].y == gridPos.y)) return [];
		visited.push(gridPos);
		
		var neighbours_a = this.neighbours(gridPos);
		for (var i = 0; i < neighbours_a.length; i++) {
			if (this.isOccupied(neighbours_a[i])) 								emptySlots = emptySlots.concat(this.validEmptyNeighbours(thisPlayer,neighbours_a[i],visited)); //branch node in recursion
			else if (!this.hasNeighboursOfPlayer(neighbours_a[i],oppPlayer)) 	emptySlots.push(neighbours_a[i]); //leaf node in recursion
		}
		
		return emptySlots;
	}
	
	this.getPieceInGridPos = function(gridPos) {
		for (var i = 0; i < this.pieces.length; i++) {
			if (this.pieces[i].gridPos.equals(gridPos)) return this.pieces[i];
		}
		return undefined;
	}
	
	this.hasNeighboursOfPlayer = function(gridPos,player) {
		var neighbours_a = this.neighbours(gridPos);
		for (var i = 0; i < neighbours_a.length; i++) {
			var thisPiece = this.getPieceInGridPos(neighbours_a[i]);
			if ((thisPiece instanceof Piece) && (thisPiece.playerId == player)) return true;
		}
		return false;
	}
}


function drawDotOnGridPos(gridPos_a) { // requires noLoop();
	fill(255);
	for (var i = 0; i < gridPos_a.length; i++) {
		var pos = translateGrid2Pos(gridPos_a[i]);
		ellipse(pos.x,pos.y,10,10);
	}
}



function Piece(insect,col,row,playerId) {
	this.insect = insect||'n/a';
	this.gridPos = createVector(col||0,row||0); // grid-position is a vector described in COLUMN and ROW
	this.playerId = playerId||0;	// 0 = me ; 1 = AI opponent
	
	this.setGridPos = function(gridPos) {
		this.gridPos = gridPos;
		this.hexagon.setGridPos(this.gridPos);
		this.hexagon.updatePos();
	}
	
	this.setHexagon = function(gridPos) {
		this.hexagon = new Hexagon(gridPos);
		this.hexagon.updatePos(); // hexagon's pos is described in PIXELS. so the gridPos needs to be translated to pixels
		this.hexagon.setCaption(this.insect+" / "+this.gridPos.x+","+this.gridPos.y);
	}
	
	this.drawHexagon = function () {
		if (this != draggingPiece) this.hexagon.updatePos(); // only snap the hexagon back to grid when this piece is not being dragged
		this.hexagon.draw(pieceColors[this.playerId]);
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
	
	this.setGridPos = function(gridPos) {
		this.gridPos = gridPos || createVector(0,0);
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

function translateGrid2Pos(grid) {
	var xPos = grid.x*hexHoffset;
	xPos = xPos + width/2;
	var yPos = grid.y * hexHeight;
	yPos = yPos + Math.abs(grid.x%2) * hexVoffset; //adding or not adding vertical offset
	yPos = yPos + height/2;
	return createVector(xPos,yPos);
}


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

function isInsideHex(hexagon) {
	//if the mouse mointer is inside a hexagon given by coordinates of it's center and width/height
	// source http://www.playchilla.com/how-to-check-if-a-point-is-inside-a-hexagon
	var hori = hexWidth/4;
	var vert = hexHeight/2;
	var h = hexagon;
	var q2x = Math.abs(mouseX - h.pos.x);			// transform the test point locally and to quadrant 2
	var q2y = Math.abs(mouseY - h.pos.y);			// transform the test point locally and to quadrant 2
	if ((q2x > hori*2) || (q2y > vert)) return false;			// bounding test (since q2 is in quadrant 2 only 2 tests are needed)
	return vert * 2 * hori - vert * q2x - hori * q2y >= 0;	// finally the dot product can be reduced to this due to the hexagon symmetry
}


function gridPosUnderMouse() {
	var m_x = mouseX - width/2 - hexWidth/2;
	var m_y = mouseY - height/2 - hexHeight/2;
	var x = m_x / (hexWidth * 0.75);
	var y = (m_y - Math.abs(Math.ceil(x)%2) * hexVoffset) / hexHeight;
	var xGridPos = Math.ceil(x);
	var yGridPos = Math.ceil(y);
	
	//we are using a square here. square emcompasses the hexagon at (x,y) gridPos but also parts of (x+1,y) and (x+1,y+1)
	//(x,y) is the most likey answer because the square above encompasses 75% + 12.5% of it. the rest is divided into the triangles for the other two 
	// so here we compare distance between the center of (x,y) and the mouse and comopare to (x+1,y) and (x+1,y+1)
	
	//put all 3 distances into an array, get the smallest distance and store in pos_v
	var mouse_v = createVector(mouseX,mouseY);
	var pos1_v = createVector(xGridPos,yGridPos);
	var pos2_v = createVector(xGridPos+1,yGridPos+Math.abs(xGridPos%2));
	var pos3_v = createVector(xGridPos+1,yGridPos+Math.abs(xGridPos%2)-1);
	var posValues_a = [pos1_v,pos2_v,pos3_v];
	var dist_a = [dista(translateGrid2Pos(pos1_v),mouse_v), // distance form (x,y)
				dista(translateGrid2Pos(pos2_v),mouse_v), // distance form (x+1,y)
				dista(translateGrid2Pos(pos3_v),mouse_v) // distance form (x+1,y+1)
		];
	var pos_v = posValues_a[indexOfSmallestVal(dist_a)];
	
	return pos_v;
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


function mouseDragged(event) {
	
  if (draggingPiece instanceof Piece) { //if a piece is being dragged, update it's hexagon's pixels
	  if (isInsideHex(draggingPiece.hexagon)) {
		  draggingPiece.hexagon.pos = createVector(mouseX,mouseY);
	  }
	  else { // if mouse is not inside any hexagon anymore, reset
		draggingPiece.hexagon.updatePos();
		draggingPiece = undefined;
		drawEmptyNeighbors = undefined;
	  }
  }
  else {  //if no piece yet in dragging, check if mouse is over a piece
		pieces = boards[0].pieces; // assumption of only one board
		var mouseInsideAnyHex = false;
		for (var i = 0; i < pieces.length; i++) {
			if (isInsideHex(pieces[i].hexagon))	{
				draggingPiece = pieces[i];
				mouseInsideAnyHex = true;
				drawEmptyNeighbors = boards[0].validEmptyNeighbours(draggingPiece.playerId);
			}
		}

		
		/*
		fill(255,0,255);
		ellipse(translateGrid2Pos(pos1_v).x,translateGrid2Pos(pos1_v).y,10,10);
		fill(0,120,255);
		ellipse(translateGrid2Pos(pos2_v).x,translateGrid2Pos(pos2_v).y,10,10);
		fill(255,120,0);
		ellipse(translateGrid2Pos(pos3_v).x,translateGrid2Pos(pos3_v).y,10,10);
		console.log(dist_a);
		*/
		
		/*
		var pos_v = gridPosUnderMouse();	
		noLoop();
		var colorR = map (pos_v.x,-3,3,0,255);
		var colorG = map (pos_v.y,-3,3,0,255);
		fill(colorR,colorG,0);
		noStroke();
		ellipse(mouseX,mouseY,5,5);
		*/

	}
	return false;
}

function mouseReleased() {
	if (draggingPiece instanceof Piece) {
		var snapToPos = gridPosUnderMouse();
		draggingPiece.setGridPos(snapToPos);
		drawEmptyNeighbors = undefined;
	}
}

function dista(v1,v2) {
	var dx = v2.x - v1.x;
    var dy = v2.y - v1.y;
    return Math.sqrt(dx*dx + dy*dy);
}
function indexOfSmallestVal(_a){
	return _a.reduce((iMin, x, i, arr) => x < arr[iMin] ? i : iMin, 0);
}




function mousePressed() {

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
