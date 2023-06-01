let pause_Button;
let play_Button;
let stop_Button;
let skip_start_Button;
let skip_end_Button;
let loop_Button;
let record_Button;
let column_Position_Button = 30;

let cuf_off_Slider;
let resonance_Slider;
let dry_wet_Slider;
let output_level_Slider;

let play_Buttons = [
                [pause_Button, "pause", 10, column_Position_Button, player_pause],
                [play_Button, "play", 70, column_Position_Button, player_play],
                [stop_Button, "stop", 120, column_Position_Button, player_stop],
                [skip_start_Button, "skip to start", 170, column_Position_Button, player_skip_start],
                [skip_end_Button, "skip to end", 260, column_Position_Button, player_skip_end],
                [loop_Button, "loop", 350, column_Position_Button, player_loop],
                [record_Button, "record", 400, column_Position_Button, player_record]    
];

let lowpass_Filter_Texts = [
//    ["low-pass filter", 20, 70],
//    ["cufoff\nfrequency", 10, 100 - 10],
//    ["resonance", 10 + 60, 100 - 10],
//    ["dry/\nwet", 10 , 100 + 180 - 10],
//    ["output\nlevel", 10 + 60, 100 + 180 - 10]    
    
    ["cufoff frequency", 10, 100 - 10],
    ["resonance", 10, 150 - 10],
    ["dry / wet", 10, 200 - 10],
    ["output level", 10, 250 - 10]    
];

let lowpass_Filter_Sliders = [
//    [cuf_off_Slider,      0, 20000, 10000, 10, -20 - 200, 440],
//    [resonance_Slider,    0, 1000, 50, 1, -20 - 200, 380],
//    [dry_wet_Slider,      0, 1, 0.5, 0.1, 160 - 200, 440],
//    [output_level_Slider, 0, 1, 0.5, 0.1, 160 - 200, 380]
    
    [cuf_off_Slider, 0, 20000, 10000, 10, 10, 100],
    [resonance_Slider, 0, 1000, 50, 1, 10, 150],
    [dry_wet_Slider, 0, 1, 0.5, 0.1, 10, 200],
    [output_level_Slider, 0, 1, 0.5 , 0.1, 10, 250]    
];

let attack_Slider;
let knee_Slider;
let release_Slider;
let ratio_Slider;
let threshold_Slider;
let dry_wet2_Slider;
let output2_Slider;
let dynamic_Composer_Slider_Row = 240;
let dynamic_Composer_Text_Row = 170;


let master_Volume_Slider;
let master_Volume_Sliders = [
    [master_Volume_Slider, 0, 1, 0.5, 0.1, dynamic_Composer_Slider_Row + 200, 100]
];


let dynamic_Composer_Sliders = [
    [attack_Slider, 0, 1, 0.5, 0.1, dynamic_Composer_Slider_Row, 100],
    [knee_Slider, 0, 40, 20, 1, dynamic_Composer_Slider_Row, 150],
    [release_Slider, 0, 1, 0.5, 0.1, dynamic_Composer_Slider_Row, 200],
    [ratio_Slider, 0, 20, 10, 1, dynamic_Composer_Slider_Row, 250],
    [threshold_Slider, -100, 0 , -50, 1, dynamic_Composer_Slider_Row, 300],
    [dry_wet2_Slider, 0, 1, 0.5, 0.1, dynamic_Composer_Slider_Row, 350],
    [output2_Slider, 0, 1, 0.5, 0.1, dynamic_Composer_Slider_Row, 400]
];
let dynamic_Composer_Texts = [
    ["dynamic compressor", 200, 70],    
    ["attack", dynamic_Composer_Text_Row, 100],
    ["knee", dynamic_Composer_Text_Row, 150],
    ["release", dynamic_Composer_Text_Row, 200],
    ["ratio", dynamic_Composer_Text_Row, 250],
    ["threshold", dynamic_Composer_Text_Row, 300],
    ["dry / wet", dynamic_Composer_Text_Row, 350],
    ["output level", dynamic_Composer_Text_Row, 400],

    ["master volume", 450, 70]
];

let reverb_Texts = [
    ["reverb", 20, 450],
    ["reverb\nduration", 10, 380 + 100 - 10],
    ["delay\nrate", 10, 380 + 100 - 10 + 50],
    ["dry/\nwet", 10 , 380 + 100 - 10 + 150],
    ["output\nlevel", 10, 380 + 100 - 10 + 200]            
]

let isReversed = false;
let reverse_Button;
let reverb_Buttons = [
    [reverse_Button, "reverse", 10, 580, toggleReversed]    
];

let reverb_Duration_Slider;
let decay_Rate_Slider;
let dry_wet3_Slider;
let output3_Slider;

let reverb_Sliders = [
    [reverb_Duration_Slider, 0, 10, 5, 1, 10 + 50, 380 + 100 ],
    [decay_Rate_Slider, 0, 100, 50, 10, 10 + 50, 380 + 100 + 60],
    
    [dry_wet3_Slider, 0, 1, 0.5, 0.1, 10 + 50, 380 + 100 + 160],
    [output3_Slider, 0, 1, 0.5, 0.1, 10 + 50, 380 + 100 + 200]    
];

let Waveshaper_Distortion_Texts = [
    ["waveshaper distortion", 220, 450],
    ["distortion\namount", 200+10, 380 + 100 - 10],
    ["oversample", 200+10, 380 + 100 - 10 + 50],
    ["dry/\nwet", 200+10 , 380 + 100 - 10 + 100],
    ["output\nlevel", 200+10, 380 + 100 - 10 + 150]                
]

let Distortion_Amount_Slider;
let Oversample_Slider;
let dry_wet4_Slider;
let output4_Slider;

let Waveshaper_Distortion_Sliders = [
    [Distortion_Amount_Slider, 0, 1, 0.5, 0.1, 270, 380 + 100 ],
    [Oversample_Slider, 0, 2, 0, 0.1, 270, 380 + 100 + 50],
    [dry_wet4_Slider, 0, 1, 0.5, 0.1, 270, 380 + 100 + 100],
    [output4_Slider, 0, 1, 0.5, 0.1, 270, 380 + 100 + 150]        
];


let Spectrum_Texts = [
    ["Spectrum In", 400+20, 380 + 100 - 10],
    ["Spectrum Out", 400+20, 380 + 100 - 10 + 100],    
];

let total_Buttons = [
    play_Buttons,
    reverb_Buttons
]

let total_Sliders = [
    dynamic_Composer_Sliders,
    
    master_Volume_Sliders,
    
    reverb_Sliders,
    Waveshaper_Distortion_Sliders
];
let total_Texts = [
    lowpass_Filter_Texts,
    dynamic_Composer_Texts,
    reverb_Texts,
    Waveshaper_Distortion_Texts,
    Spectrum_Texts
]

let player;
let recorder;
let recording;
let outFile;


function preload() {
    player = loadSound("../sounds/AfterLIKE.mp3");
}

function setup() {
  // put setup code here
    var canv = createCanvas(600, 800);
    background(0, 255, 0);  

    setup_GUI();
    setup_Filters();
}

function draw() {
  // put drawing code here
    update_Filter_Effects();
}

let low_pass_Filter;
let Wave_Shaper_Distortion;
let dynamic_Compressor;
function setup_Filters() {
    
    low_pass_Filter = new p5.LowPass();
    Wave_Shaper_Distortion = new p5.Distortion();
    
    dynamic_Compressor = new p5.Compressor();
    
    reverb_Filter = new p5.Reverb();
    master_Volume = new p5.Gain();
  
    
    player.disconnect();
    low_pass_Filter.disconnect();
    low_pass_Filter.process(player);
    Wave_Shaper_Distortion.disconnect();
    Wave_Shaper_Distortion.process(low_pass_Filter);

    dynamic_Compressor.disconnect();
    dynamic_Compressor.process(Wave_Shaper_Distortion);
    
    reverb_Filter.disconnect();
    reverb_Filter.process(dynamic_Compressor);
    
    
    master_Volume.connect();    
//    master_Volume.setInput(Wave_Shaper_Distortion);    
//    master_Volume.setInput(dynamic_Compressor);    
    master_Volume.setInput(reverb_Filter);    
}

function setup_Recorder() {
    recorder = new p5.SoundRecorder();
    recorder.setInput(player);
    recording = false;
    outFile = new p5.SoundFile();        
}

function setup_GUI() {
    for(let i=0; i<lowpass_Filter_Sliders.length; ++i) {

//        let d = createDiv();
//        d.style('transform: rotate(' + 90 + 'deg);');       
        lowpass_Filter_Sliders[i][0] = createSlider(
            lowpass_Filter_Sliders[i][1],
            lowpass_Filter_Sliders[i][2],
            lowpass_Filter_Sliders[i][3],
            lowpass_Filter_Sliders[i][4]
        );
        lowpass_Filter_Sliders[i][0].position(
            lowpass_Filter_Sliders[i][5],
            lowpass_Filter_Sliders[i][6]        
        );
//        d.child(lowpass_Filter_Sliders[i][0]);

    }

    
    
    
    for(let i=0; i<total_Buttons.length; ++i) 
        for(let j=0;j<total_Buttons[i].length;++j) {
            total_Buttons[i][j][0] = createButton(total_Buttons[i][j][1]);
            total_Buttons[i][j][0].position(
                total_Buttons[i][j][2], 
                total_Buttons[i][j][3]
            );
            total_Buttons[i][j][0].mousePressed(total_Buttons[i][j][4]);
            
    }
    

    for(let i=0; i<total_Texts.length;++i)
        for(let j=0; j<total_Texts[i].length;++j) {
            text(
                total_Texts[i][j][0],
                total_Texts[i][j][1],
                total_Texts[i][j][2]
            );
        }

    for(let i=0;i<total_Sliders.length;++i) 
        for(let j=0;j<total_Sliders[i].length;++j)  {
            total_Sliders[i][j][0] = createSlider(
                total_Sliders[i][j][1],
                total_Sliders[i][j][2],
                total_Sliders[i][j][3],
                total_Sliders[i][j][4]            
            );
            total_Sliders[i][j][0].position(
                total_Sliders[i][j][5],
                total_Sliders[i][j][6]            
            )
        }
    
}

function player_pause() {
    player.pause();
}
function player_play() {
    player.play();
}
function player_stop() {
    player.stop();
}
function player_skip_start() {
    player.jump(0);
}
function player_skip_end() {
    player.jump(player.duration() - 1);
}
function player_loop() {
    player.loop();
}
function player_record() {
    if(!recording) {
        console.log("start");
        recording = true;
        recorder.record(outFile);
    }
    else {
        console.log("end");        
        recording = false;
        recorder.stop();
        outFile.play();
        //save(outFile, "output.wav");
    }
}

function toggleReversed() {
    isReversed = !isReversed;
    console.log(isReversed);    
}
function update_Filter_Effects() {
    //console.log(lowpass_Filter_Sliders[3][0].value());
    low_pass_Filter.set(
        lowpass_Filter_Sliders[0][0].value(), 
        lowpass_Filter_Sliders[1][0].value()         
    );
    low_pass_Filter.drywet(lowpass_Filter_Sliders[2][0].value());
    low_pass_Filter.amp(lowpass_Filter_Sliders[3][0].value());
    
    Wave_Shaper_Distortion.set(
        Waveshaper_Distortion_Sliders[0][0].value(),
        Waveshaper_Distortion_Sliders[1][0].value()
    );
    Wave_Shaper_Distortion.drywet(Waveshaper_Distortion_Sliders[2][0].value());
    Wave_Shaper_Distortion.amp(Waveshaper_Distortion_Sliders[3][0].value());
    
    dynamic_Compressor.set(
        dynamic_Composer_Sliders[0][0].value(),
        dynamic_Composer_Sliders[1][0].value(),        
    );
    dynamic_Compressor.drywet(dynamic_Composer_Sliders[5][0].value());
    dynamic_Compressor.amp(dynamic_Composer_Sliders[6][0].value());
    
 //   reverb_Filter.set(
//        reverb_Sliders[0][0].value(),
//        reverb_Sliders[1][0].value(),
//        isReversed
//    );
    reverb_Filter.drywet(reverb_Sliders[2][0].value());
    reverb_Filter.amp(reverb_Sliders[3][0].value());
    
    master_Volume.amp(master_Volume_Sliders[0][0].value());
}
