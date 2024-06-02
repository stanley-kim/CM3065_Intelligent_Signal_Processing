# End Term Exercise3

### Description

    The application must run on a Jupyter notebook written in Python, use ffprobe to examine the files, and ffmpeg to convert the films.

    The application should automatically convert the submitted films with an incorrect format. The program will create a new copy of the films by adding ‘_formatOK’ at the end of the name. 

    The format of the films specified by the festival organisation is:
    - Video format (container): mp4
    - Video codec: h.264
    - Audio codec: aac
    - Frame rate: 25 FPS
    - Aspect ratio: 16:9
    - Resolution: 640 x 360
    - Video bit rate: 2 – 5 Mb/s
    - Audio bit rate: up to 256 kb/s
    - Audio channels: stereo

### The Result
|Filename|Original|Converted|
|---|---|---|
|Cosmos_War_of_the_Planets.mp4|video format mp4=>satisfied|mp4=>satisfied|
||video code: h264=>safisfied|h264=>safisfied|
||audio codec: aac=>satisfied|aac=>satisfied|
||video frame rate: 29.970-->Not safisfied|25.0=>safisfied|
||video aspect ratio: 314:177-->Not satisfied|16:9=>satisfied|
||video resolution: 628x354-->Not satisfied|640x360=>satisfied|
||video bit rate(Mb/s): 2.989=>satisfied|2.971=>satisfied|
||audio bit rate(kb/s): 317.103-->Not satisfied|129.606=>satisfied|
||audio channels: stereo=>satisfied|stereo=>satisfied|
|The_Gun_and_the_Pulpit.avi|video format avi-->Not satisfied|mp4=>satisfied|
||video code: rawvideo-->Not safisfied|h264=>safisfied|
||audio codec: pcm_s161e-->Not satisfied|aac=>satisfied|
||video frame rate: 25.0=>safisfied|25.0=>safisfied|
||video aspect ratio: 180:101-->Not satisfied|16:9=>satisfied|
||video resolution: 720x404-->Not satisfied|640x360=>satisfied|
||video bit rate(Mb/s): 87.439-->Not satisfied|2.837=>satisfied|
||audio bit rate(kb/s): 1536.0-->Not satisfied|128.424=>satisfied|
||audio channels: stereo=>satisfied|stereo=>satisfied|

    - How ffprobe and ffmpeg has been installed and configured 
        I used codes in Week20 exercise20 
        Download ffmpeg and ffprobe by curl utility  
        Extract ffmpeg.tar.gz  
        Use it 
    - Filename: Exercise3.ipynb
        my application converts submitted movies as required format movies. 
        By callling generate_Movie_File function, the movies are converted as below. 
        "_formatOK" is added to the new movie name 

