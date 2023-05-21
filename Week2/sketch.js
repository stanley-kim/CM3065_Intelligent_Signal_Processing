let mySound;
let playStopButton;
let jumpButton;
let sliderVolume;
let sliderRate;
let sliderPan;

function preload() {
    soundFormats('mp3');
    mySound = loadSound('./sounds/AfterLIKE');    
}

function setup() {
  // put setup code here
    createCanvas(400, 400);
    background(180);
    
    playStopButton = createButton('play');
    playStopButton.position(200, 20);
    playStopButton.mousePressed(playStopSound);
    jumpButton = createButton('jump');
    jumpButton.position(250, 20);
    jumpButton.mousePressed(jumpSound);
    
    sliderVolume = createSlider(0, 2, 1, 0.01);
    sliderVolume.position(20, 20);
    text('volume', 80, 20);
    sliderRate = createSlider(-2, 2, 1, 0.01);
    sliderRate.position(20, 70);
    text('rate', 80, 65);
    sliderPan = createSlider(-1, 1, 0, 0.01);
    sliderPan.position(20, 115);
    text('pan', 80, 110);
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

function jumpSound() {
    let dur = mySound.duration();
    let t = random(dur);
    mySound.jump(t);
    console.log(t);
}

function draw() {
  // put drawing code here
    mySound.setVolume(sliderVolume.value());
    mySound.rate(sliderRate.value());
    mySound.pan(sliderPan.value());
}
