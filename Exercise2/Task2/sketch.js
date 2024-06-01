//this application is based on the 4.108 Exercise 8 Real-time audio visualisations with JavaScript

var mySound;
var playStopButton;
var jumpButton;
var sliderVolume;
var sliderRate;
var sliderPan;

var fft;

var analyzer;

var rms_Length = 0; 
var spectralCentroid_Size = 0;
var spectralRolloff_Color = 0;

var zcr_Color = 0;
var spectralFlatness_Width = 0;
var spectralSpread_Alpha = 0;

var myRec;

var set_bgcolor;
var bgcolor = 0;
function preload() {
//  soundFormats('wav', 'mp3');
  soundFormats('mp3');
  mySound = loadSound('/sounds/Kalte_Ohren_(_Remix_)');
}

function setup() {
  createCanvas(420, 500);
  bgcolor = 'gray'
  //background(bgcolor);
    
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

  if(typeof Meyda === "undefined") {
    console.log("Meyda could not be found!");
  } else {
    analyzer = Meyda.createMeydaAnalyzer({
      "audioContext": getAudioContext(),
      "source": mySound,
      "bufferSize": 512, 
      "featureExtractors": [
        "rms", 
        "zcr",
        "amplitudeSpectrum",
        "loudness",
        "spectralCentroid",
        "spectralRolloff",
        "spectralFlatness",
        "spectralSpread",
        "spectralCrest"
      ],

      "callback": features => {
//        console.log(features);
        rms_Length = features.rms * 3000;
        spectralCentroid_Size = map(features.spectralCentroid, 0, 44100 / 500, 0, 200);
        spectralRolloff_Color = map(features.spectralRolloff, 0, 44100 / 2, 0, 255); 
        zcr_Color = map(features.zcr, 0, 255, 0, 255);
        spectralFlatness_Width = map(features.spectralFlatness, 0, 1, 1, 100);
        spectralSpread_Alpha = (features.spectralSpread * 4) % 256;
      }
    });
  }


  set_bgcolor = createStringDict({
    'black': true,
    'white': true,
    'red': true,
    'gray': true
  });

  myRec = new p5.SpeechRec('en-US', parseWords);
  myRec.continuous = true;
  myRec.interimResults = true;
  myRec.start();
  console.log('Speech Recognition Start');
}

function parseWords() {
  var mostrecentword = myRec.resultString.split(' ').pop().toLowerCase();
  console.log(mostrecentword);

  if (set_bgcolor.hasKey(mostrecentword)) 
    bgcolor = mostrecentword;
}
function draw() {
  background(bgcolor);
  fill('blue');
  rect(300, 480, 80, 20);
  fill('white');
  text('bgcolor: ' + bgcolor, 300, 492);    

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
    
  noStroke();
  text('RMS:', 20,250);
  text('Num of Rects', 20,260);
  fill('blue');
  for(let i=0; (70 * i) < rms_Length ;++i) 
    rect(20, 280 + 10 * i , 50, 8); 
  
  noStroke();
  fill('black');
  text('spectralRolloff: Color', 105,250);
  text('spectralCentroid: Rect Size', 105,270);
  fill(spectralRolloff_Color, 255 - spectralRolloff_Color, (spectralRolloff_Color * 5) % 255);
  rect(100, 280, 50, spectralCentroid_Size);

  fill('black');
  text('spectralSpread: Color Opacity', 245,250);
  var new_color = color(100, 50, 100);
  new_color.setAlpha(spectralSpread_Alpha);
  fill(new_color);
  rect(300, 265, 50, 50);  
  
  fill('black');
  text('ZCR: Border Color', 235,360);
  text('spectralFlatness: Border Size', 235,380);
  stroke((zcr_Color * 10) % 255, (zcr_Color * 5) % 255, (zcr_Color * 2) % 255);
  strokeWeight(spectralFlatness_Width);
  rect(300, 410, 20, 20);
  noStroke();
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
    } else {
      //mySound.play();
      mySound.loop();
      analyzer.start();      
      playStopButton.html('stop');
    }  
}