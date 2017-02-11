var ws;
var hexagons = [];
var slider;

function setup() {
	createCanvas(600,500);
	textAlign(CENTER);
	
    ws = new WebSocket("ws://127.0.0.1:50007");
    ws.onmessage = function (evt) {
		console.log(evt)
        console.log(evt.data);
    }
	
	slider = createSlider(0,100,30);
	slider.position(10,10);
	
	setHexSize(30);
	
	
	createButton("GetBoardLayout").mousePressed(function () {
		ws.send(JSON.stringify({
			action: "getBoardLayout"
		}));
	});
	
	var hexData = [
	[0,0],
	[0,-1],
	[1,-1],
	[1,0],
	[0,1],
	[-1,0],
	[-1,-1],
	[2,0],
	[3,0],
	[-2,-1],
	[-3,-1],
	[-1,1],
	[-2,1]
	];
	
	
	for (var i = 0; i < hexData.length; i++) {
		var thisHex = new Hexagon(createVector(hexData[i][0],hexData[i][1]));
		thisHex.updatePos();
		thisHex.setCaption(i+"/"+hexData[i][0]+","+hexData[i][1]);
		hexagons.push(thisHex);
	}
}


function draw() {
	background(0);
	setHexSize(slider.value());
	
	for (var i = 0; i < hexagons.length; i++) {
		hexagons[i].updatePos();
		hexagons[i].draw();
	}
}

function Hexagon(gridPos) {
	this.gridPos = gridPos || createVector(0,0);
	this.pos = translateGrid2Pos(this.gridPos);
	this.caption = "";
	
	this.draw = function () {
		// push();
		// translate(this.pos);
		// rotate(frameCount / -100.0);
		polygon(this.pos.x, this.pos.y, hexSize, 6);
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