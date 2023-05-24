let player;

function preload() {
    player = loadSound("../sounds/AfterLIKE.mp3");
}

function setup() {
  // put setup code here
    var canv = createCanvas(200, 200);
    background(0, 255, 0);
    canv.mousePressed(mousePressed);
}

function draw() {
  // put drawing code here
}

function mousePressed() {
    player.loop();
}