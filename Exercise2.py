#                       !!
# 1111 1000  1011 1101  0011 1110  0110 1111 00110111111000001111010100111100000111110011111110000100
# 1111 1000  1011 1101    11 1110   110 1111  11011111100000111101011111001111111111110000100
# 0xf8       0xbd       0x3e       0x6f
# end Encoding 2: Sound1.wav 1002088-> Sound1_Enc.ex2 4115718
# end Encoding 4: Sound1.wav 1002088-> Sound1_Enc.ex2 1516265
# end Encoding 2: Sound2.wav 1008044-> Sound2_Enc.ex2 4348595
# end Encoding 4: Sound2.wav 1008044-> Sound2_Enc.ex2 1575347

import sys
import os
from collections import Counter

DEBUG_MODE = False
NUMBERS_TO_SHOW = 20

def convert_to_unary_format(q):
	str = ['1' for _ in range(q) ]
	str.append('0')
	return "".join(str)

def encode_to_Str_List(S, K):
	m = pow(2, K)
	q = S // m
	r = S % m
	
	encoded_list = [ convert_to_unary_format(q), format(r, "b").zfill(K)]
	#print('original: ' + format(S, "b")  +  ' encoded: ' + "".join(encoded_list))
	return encoded_list

def encode_to_Str(S, K):
	return "".join(encode_to_Str_List(S, K))

def encode_List_to_Str(S_List, K):
	encoded_List = []
	for i, S in enumerate(S_List):
		encoded_List.append(encode_to_Str(S, K))
		if DEBUG_MODE and i == 20:
			print(encoded_List)
	c = Counter(encoded_List)
	print(c)
	print("-"*30)
	if False:
		for k in sorted(c.keys()):
			element = c[k]
			print(f'{k}:{element}', end=", ")
		print(f'')
		print("-"*30)
		count_for_target = 0
		for i in range(1000000):
			encoded_Str = encode_to_Str(i, K)
			if encoded_Str not in c:
				print(f'{encoded_Str} not in c')
				count_for_target = count_for_target + 1
				if count_for_target == 5:
					break
		print("-"*30)
 
	for k in sorted(c.keys()):
		element = c[k]
		if element < 3000 and len(k) < 40 // K:
			print(f'{k}:{element}', end=", ")
	print(f'')
	print("="*30)
	for k in sorted(c.keys(), reverse=True):
		element = c[k]
		if element > 10000 and len(k) > 40 // K:
			print(f'{k}::{element}', end=", ")
	print(f'')

	return "".join(encoded_List)

def encode_File_to_Str(filename, K):
	with open(filename, 'rb') as file:
		byteBuffer = bytearray(file.read())
	for i, byte in enumerate(byteBuffer):
		if i < NUMBERS_TO_SHOW:
			print(f'byte[{i}]: {byte}')
	for i in range(NUMBERS_TO_SHOW):
		print(f'byte[{i-NUMBERS_TO_SHOW}]: {byteBuffer[i-NUMBERS_TO_SHOW]}')
	
	return encode_List_to_Str(byteBuffer, K)


def encode_File_to_File(source_filename, destination_filename, K):
	encoded_Str = encode_File_to_Str(source_filename, K)
	if not encoded_Str:
		print(f'No encoded String')
		return False
	Len_Str = len(encoded_Str)
	if Len_Str == 0:
		print(f'No encoded String to decode')
		return False
	if DEBUG_MODE:
		print(f'encoded_Str : {encoded_Str} / Length: {len(encoded_Str)}')

	if Len_Str % 8 > 0:
		new_Len	= (Len_Str // 8 + 1) * 8
		# 110001 (6) -> 1100 0100 (8)
		encoded_Str = encoded_Str.ljust(new_Len, '1')
		if DEBUG_MODE:
			print(f'encoded_Str:: {encoded_Str} / Length: {len(encoded_Str)}')

	encoded_Byte_Str_List = []
	for i in range(0, len(encoded_Str), 8):
		element_before = encoded_Str[i:i+8]
		element = eval('0b' + encoded_Str[i:i+8])
		encoded_Byte_Str_List.append(element)
		if DEBUG_MODE:
			print(f'{element_before} {element} {format(element, "x")}')
	if DEBUG_MODE:
		for byte in bytearray(encoded_Byte_Str_List):
			print(f'bytearray: {byte} {format(byte, "x")}')	
	if DEBUG_MODE:
		print(f'encoded Binary List: {encoded_Byte_Str_List}')
		print(f'encoded Binary List: {bytearray(encoded_Byte_Str_List)}')


	with open(destination_filename, 'wb') as binary_file:	
		binary_file.write( bytearray(encoded_Byte_Str_List) )
	return True
		
def decode(encoded_list, K):
	m = pow(2, K)
	decoded_list = [len(encoded_list[0]) -1, eval('0b' + encoded_list[1]) ]
	decoded = decoded_list[0] * m + decoded_list[1]
	return decoded

def decode_to_List(encoded_str, K, decoded_List):
	m = pow(2, K)
	starting_index = 0
	Len_Str = len(encoded_str)
	while True:
		if starting_index + 1 + K > Len_Str:
			break
		q = encoded_str.find('0', starting_index)
		if q < 0:
			break
		r_str = encoded_str[q + 1: q + 1 + K]
		r = eval('0b' + r_str)
		decoded_List.append( (q - starting_index) * m + r)
		starting_index = q + 1 + K 

def decode_File_to_File(source_filename, destination_filename, K):
	m = pow(2, K)
	with open(source_filename, 'rb') as file:
		byteBuffer = bytearray(file.read())
	print("reading finished")
	encoded_Str_List = [] 
	for i, byte in enumerate(byteBuffer):
		if DEBUG_MODE:
			print(f'decoded byte: {byte} {format(byte, "x")} {format(byte, "b")}')
		encoded_Str_List.append(format(byte, "b").zfill(8))
	encoded_Str_with_Zero_Padding = "".join(encoded_Str_List)
	

	if DEBUG_MODE:
		print(f'{encoded_Str_with_Zero_Padding}')

	starting_index = 0
	Len_Str_Original = len(encoded_Str_with_Zero_Padding)
	while True:
		Len_Str = Len_Str_Original - starting_index
		if Len_Str == 0:
			encoded_Str = encoded_Str_with_Zero_Padding
			break
		elif Len_Str <= K:
			encoded_Str = encoded_Str_with_Zero_Padding[:starting_index]
			break
		q = encoded_Str_with_Zero_Padding.find('0', starting_index)
		if q < 0:
			encoded_Str = encoded_Str_with_Zero_Padding[:starting_index]
			break
		starting_index = q + 1 + K
		#print(f'{starting_index}', end=" ")
#	print(f'encoded_Str: {encoded_Str} / Length {len(encoded_Str)}')	

	print("making string finished")
	result_List = []
	decode_to_List(encoded_Str, K, result_List)
	print(f'{result_List[:NUMBERS_TO_SHOW]}')
	print(f'{result_List[-NUMBERS_TO_SHOW:]}')

	with open(destination_filename, 'wb') as binary_file:
		binary_file.write( bytearray(result_List) )		

#def decode_to_str(encoded_str, K):
#	m = pow(2, K)
#	q = encoded_str.find('0')
#	r = eval('0b' + encoded_str[q + 1: q+ 1 + K])
#	return q * m + r
	
def compare_Binary_Files(filename0, filename1):
	with open(filename0, 'rb') as file0:
		byteArray0 = bytearray(file0.read())
	with open(filename1, 'rb') as file1:
		byteArray1 = bytearray(file1.read())
	if len(byteArray0) != len(byteArray1):
		print(f'two files are different {len(byteArray0)} {len(byteArray1)}')
		return False
	for byte0, byte1 in zip(byteArray0, byteArray1):
		if byte0 != byte1:
			print(f'two files are different {byte0} {byte1}')
			return False
	return True


S0 = 0b00010011
S1 = 0b00010011
#K = 4
S2 = 0b0001001100010011
S3 = 0b0001
S4 = 0b0011
S5 = 0b11111111

original_wave_filename0 = 'Sound1.wav'
original_wave_filename1 = 'Sound2.wav'

encoded_filename = 'new.hex'
decoded_filename = 'old.wav'

for original_wav_filename in ['Sound1.wav', 'Sound2.wav']:
	for K in [2, 4]:
		encoded_filename = original_wav_filename.split('.')[0] + '_Enc' + '.ex2'
		decoded_filename = original_wav_filename.split('.')[0] + '_EncDec' + '.wav' 
		encode_File_to_File(original_wav_filename, encoded_filename, K)
		print(f'end Encoding {K}: {original_wav_filename} {os.path.getsize(original_wav_filename)}-> {encoded_filename} {os.path.getsize(encoded_filename)}')
		decode_File_to_File(encoded_filename, decoded_filename, K)
		print('end Decoding')

		if compare_Binary_Files(original_wav_filename, decoded_filename):
			print(f'same files {original_wav_filename} {decoded_filename}')
		else:
			print(f'different files {original_wav_filename} {decoded_filename}')




