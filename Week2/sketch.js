let mySound;
let playStopButton;

function preload() {
    mySound = loadSound('./sounds/AfterLIKE.mp3');    
}

function setup() {
  // put setup code here
    createCanvas(400, 400);
    background(180);
    
    playStopButton = createButton('play');
    playStopButton.position(20, 20);
    playStopButton.mousePressed(playStopSound);
    
}

function playStopSound() {
    if(mySound.isPlaying()) {
        mySound.stop();
        //mySound.pause();
        playStopButton.html('play');
    }
    else {
        //mySound.play();
        mySound.loop();
        playStopButton.html('stop');        
    }
    console.log(getAudioContext().state);
}

function draw() {
  // put drawing code here
}
