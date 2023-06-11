var mySound;
var playStopButton;
var jumpButton;
var sliderVolume;
var sliderRate;
var sliderPan;

var fft;

function preload() {
  soundFormats('wav', 'mp3');
  mySound = loadSound('/sounds/233709__x86cam__130bpm-32-beat-loop_v2');
}

function setup() {
  createCanvas(400, 400);
  background(180);
    
  playStopButton = createButton('play');
  playStopButton.position(200, 20);
  playStopButton.mousePressed(playStopSound);
  jumpButton = createButton('jump');
  jumpButton.position(250, 20);
  jumpButton.mousePressed(jumpSong);

  sliderVolume = createSlider(0, 1, 1, 0.01);
  sliderVolume.position(20,25);
  sliderRate = createSlider(-2, 2, 1, 0.01);
  sliderRate.position(20,70);
  sliderPan = createSlider(-1, 1, 0, 0.01);
  sliderPan.position(20,115);
  
  fft = new p5.FFT(0.2, 2048);
}

function draw() {
  background(180, 100);

  fill(0);
  text('volume', 80,20);
  text('rate', 80,65);
  text('pan', 80,110);  
  
  let vol = Math.pow(sliderVolume.value(), 3);                  
  mySound.setVolume(vol);
  mySound.rate(sliderRate.value());
  mySound.pan(sliderPan.value());
    
  let spectrum = fft.analyze();
  
  push();
  translate(200,50);
  scale(0.33, 0.20);
  noStroke();
  fill(60);
  rect(0, 0, width, height);
  fill(255, 0, 0);
  for (let i = 0; i< spectrum.length; i++){
    let x = map(i, 0, spectrum.length, 0, width);
    let h = -height + map(spectrum[i], 0, 255, height, 0);
    rect(x, height, width/spectrum.length, h);
  }
  pop();
    
  fill(30, 30, 255, 200);
  let treble = fft.getEnergy("treble");
  let lowMid = fft.getEnergy("lowMid");
  let mid = fft.getEnergy("mid");
  let highMid = fft.getEnergy("highMid");
  arc(200, 275, treble, treble, 0, HALF_PI);
  fill(100, 55, 255, 200);
  arc(200, 275, lowMid, lowMid, HALF_PI, PI);
  fill(55, 100, 255, 200);
  arc(200, 275, mid, mid, PI, PI+HALF_PI);
  fill(130, 130, 255, 200);
  arc(200, 275, highMid, highMid, PI+HALF_PI, 2*PI);
}

function jumpSong() {
  var dur = mySound.duration();
  var t = random(dur);
  mySound.jump(t);
}

function playStopSound() {
  if (mySound.isPlaying())
    {
      mySound.stop();
      //mySound.pause();
      playStopButton.html('play');
      background(180);
    } else {
      //mySound.play();
      mySound.loop()            
      playStopButton.html('stop');
    }  
}