import wave
with wave.open("Ex3_sound1.wav", mode='rb') as music:
    frame_bytes = bytearray(music.readframes(music.getnframes()))    
bits_extracted = [frame_byte & 0x1 for frame_byte in frame_bytes]

chars = []
for bits8 in [bits_extracted[i: i+ 8] for i in range(0, len(bits_extracted), 8)]:
    each_char = chr(eval('0b' + "".join(map(str, bits8))))
    if each_char != '#':
        chars.append(each_char)
    else:
        break
print(f'hidden message ({"".join(chars)})')



