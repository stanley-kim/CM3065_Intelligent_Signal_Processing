var mySound;
var playStopButton;
var jumpButton;
var sliderVolume;
var sliderRate;
var sliderPan;

var fft;

var analyzer;
var rms_Row; 
var spectralCentroid_Color;

function preload() {
//  soundFormats('wav', 'mp3');
  soundFormats('mp3');

//  mySound = loadSound('/sounds/233709__x86cam__130bpm-32-beat-loop_v2');
//  mySound = loadSound('/sounds/Ex2_sound1');
  mySound = loadSound('/sounds/Kalte_Ohren_(_Remix_)');
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

  circleSize = 0;
  if(typeof Meyda === "undefined") {
    console.log("Meyda could not be found!");
  } else {
    analyzer = Meyda.createMeydaAnalyzer({
      "audioContext": getAudioContext(),
      "source": mySound,
      "bufferSize": 512, //44100 / 512 86? 
      "featureExtractors": [
        "rms", 
        "zcr",
        "amplitudeSpectrum",
        "loudness",
        "spectralCentroid",
        "spectralSpread",
        "spectralCrest"
      ],

      "callback": features => {
        console.log(features);
        rms_Row = features.rms * 3000;
        spectralCentroid_Color = features.spectralCentroid * 50;
      }
    });
  }
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
    
  //fill(30, 30, 255, 200);
  fill(spectralCentroid_Color, 300, 255);
  let treble = fft.getEnergy("treble");
  let lowMid = fft.getEnergy("lowMid");
  let mid = fft.getEnergy("mid");
  let highMid = fft.getEnergy("highMid");
  //arc(200, 275, circleSize, circleSize, 0, HALF_PI);
  ///rect(50, 275, 50, rms_Row);
  if(rms_Row > 0)
    rect(50, 270, 50, 10);
  if(rms_Row > 100)
    rect(50, 290, 50, 10);
  if(rms_Row > 2 * 100)
    rect(50, 310, 50, 10);
  if(rms_Row > 3 * 100)
    rect(50, 330, 50, 10);
  if(rms_Row > 4 * 100)
    rect(50, 350, 50, 10);

  
/*
  arc(200, 275, treble, treble, 0, HALF_PI);
  fill(100, 55, 255, 200);
  arc(200, 275, lowMid, lowMid, HALF_PI, PI);
  fill(55, 100, 255, 200);
  arc(200, 275, mid, mid, PI, PI+HALF_PI);
  fill(130, 130, 255, 200);
  arc(200, 275, highMid, highMid, PI+HALF_PI, 2*PI);
  */
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
      analyzer.stop();
      //mySound.pause();
      playStopButton.html('play');
      background(180);
    } else {
      //mySound.play();
      mySound.loop();
      analyzer.start();      
      playStopButton.html('stop');
    }  
}
