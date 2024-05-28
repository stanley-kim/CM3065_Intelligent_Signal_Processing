import wave

def decode_File(FILENAME):    
    with wave.open(FILENAME, mode='rb') as music:        
        frame_bytes = bytes(music.readframes(music.getnframes()))
        
    bits_extracted = [frame_byte & 0x1 for frame_byte in frame_bytes]

    chars = []
    for bits8 in [bits_extracted[i: i+ 8] for i in range(0, len(bits_extracted), 8)]:
        each_char = chr(eval('0b' + "".join(map(str, bits8))))
        if each_char != '#':
            chars.append(each_char)
        else:
            break
    return "".join(chars)

def encode_File(FILENAME, NEW_FILENAME, MESSAGE):
    with wave.open(FILENAME, mode='rb') as music:        
        frame_bytes = bytes(music.readframes(music.getnframes()))        
        music_params = music.getparams()

    bits = map(int, "".join([bin(ord(chr))[2:].rjust(8,'0') for chr in MESSAGE + '#']))
    
    new_frame_bytes = bytes((0xFE & frame) + (0x1 & bit) for frame, bit in zip(frame_bytes, bits))

    with wave.open(NEW_FILENAME, 'wb') as music:
        music.setparams(music_params)
        music.writeframes(new_frame_bytes)

SECRET_MESSAGE = 'Father Christmas does not exist'
SOURCE_FILE = "Ex3_sound5.wav"
MODIFIED_FILE = "modified_" + SOURCE_FILE
encode_File(SOURCE_FILE, MODIFIED_FILE, SECRET_MESSAGE)
decoded = decode_File(MODIFIED_FILE)

print(f'hidden message ({decoded})')

