# End Term Exercise2

### Description
    To create your own application (exercise 2) for encoding and decoding a series of uncompressed audio files (WAV files). 

    The application must run on a Jupyter notebook written in Python and be based on the lossless data compression method ‘Rice coding’

### The Result

|If K=4|Original File Size<br>(Bytes)|Original Rice Encoding<br>(K=4 bits)|Modified Rice Encoding<br>(K=4 bits)|Original Rice Compression Ratio<br>(K=4 bits)|Modified Rice Compression Ratio<br>(K=4 bits)|
|---|---|---|---|---|---|
|Sound1.wav|1,002,088|1,516,265|1,090,312|-51.31%(increased)|-7.83%(increased)|
|Sound2.wav|1,008,044|1,575,347|1,429,026|-56.28%(increased)|-41.82%(increased)|


|If K=2|Original File Size<br>(Bytes)|Original Rice Encoding<br>(K=2 bits)|Modified Rice Encoding<br>(K=2 bits)|Original Rice Compression Ratio<br>(K=2 bits)|Modified Rice Compression Ratio<br>(K=2 bits)|
|---|---|---|---|---|---|
|Sound1.wav|1,002,088|4,1115,718|2,288,790|-310.71%(increased)|-128.46%(increased)|
|Sound2.wav|1,008,044|4,348,595|3,746,243|-331.39%(increased)|-271.72%(increased)|

    - The analysis of the result 
        All the cases, with modified encoding(replace method), the size of encoded file is reduced  
        the size of encoded file is reduced from 1516265 bytes to 1080312 bytes in sound1.wav (K=4) 
        the size of encoded file is reduced from 4115718 bytes to 2288790 bytes in sound1.wav (K=2) 
        the size of encoded file is reduced from 1575347 bytes to 1429026 bytes in sound2.wav (K=4) 
        the size of encoded file is reduced from 4348595 bytes to 3746243 bytes in sound2.wav (K=2) 

    - The Application Summary 
        This application encodes original wav file in encode_File_to_File function 
        And it decodes ex2 file in decode_File_to_File

        Filename (notebook version): Exercise2.ipynb (notebook version), Exercise2.py(py version)

        Encode_File_to_File function 
            all bytes in wav file -> rice encoding -> one merged encoded string –convert to binary --> binary array -- write in file --> Enc.ex2 file

        Decode_File_to_File function 
            Each byte in Enc.ex2 file –merge into one string--> one merged encoded string – rice decoding -> binary array -> write in file -> EncDec.wav file  

    - A description of the modified rice encoding (replace method) 
        The replacement long length and high frequency encoded number with short length and low frequency encoded number 

        What is long length and High frequency encoded number? 
            the rice encoded number which has long length and high frequency in encoded file.  
            e.g. when file is Sound1.wav and K = 4, "11111111111111101111" appears 160358 times 

        What is  short length and low frequency encoded number? 
            The rice encoded number which has short length and low frequency in encoded file 
            e.g. when file is Sound1.wav and K = 4, "100010" appears 2893 times 

        The idea 
            If we can replace long length and high frequncy number with short length and low frequency number in the encoded file, then the lenght of encoded file can be reduced. 

        The way how to replace 
            Counter in python 
                My application uses Counter in python to count encoded numbers' frequencies. 
            List of long length and high frequency (LLHF) numbers 
                e.g when file is Sound1.wav and K=4, "11111111111111101111" is one of the element of list 
            List of short lenght and low frequncy(SLLF) numbers 
                e.g when file is Sound1.wav and K=4, "100010" is one of the element of list 
            Dictionary for replacement 
                The elements are (key: LLHF number, value: SLLF number) 
                e.g. (key: "11111111111111101111", value: "100010") 
                
                Another elements are (key: SLLF number, LLHF number) 
                e.g. (key: "100010", value: "11111111111111101111") 
            Replacement in encoding process  
                Replace encoded string based on the dictionary for replacement 
                e.g. when the encoded string is "100010" then replace this str with "11111111111111101111" by the dictonary 

                Save dictionary as pickle file to use same dictionary in decoding process 
            Replacement in decoding process 
                Load pickle file to use in decoding process 
                Fill pickle file data into dictionary dictionary 
                Same as replacement in encoding prcess 
                Replace decoded string based on the dictonary for replacement 
                    e.g. when the encoded string is "11111111111111101111" then replace this str with  "100010"  by the dictonary 
