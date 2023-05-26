let pause_Button;
let play_Button;
let stop_Button;
let skip_start_Button;
let skip_end_Button;
let loop_Button;
let record_Button;

let Buttons = [
                [pause_Button, "pause", 10, 20],
                [play_Button, "play", 70, 20],
                [stop_Button, "stop", 120, 20],
                [skip_start_Button, "skip to start", 170, 20],
                [skip_end_Button, "skip to end", 260, 20],
                [loop_Button, "loop", 350, 20],
                [record_Button, "record", 400, 20]    
              ];


function setup() {
  // put setup code here
    var canv = createCanvas(500, 500);
    background(0, 255, 0);  
    for(let i=0; i<Buttons.length; ++i) {
        Buttons[i][0] = createButton(Buttons[i][1]);
        Buttons[i][0].position(Buttons[i][2], Buttons[i][3]);

    }
}
function draw() {
  // put drawing code here
}

