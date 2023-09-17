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
import pickle

DEBUG_MODE = False
NUMBERS_TO_SHOW = 20

g_Dict_for_encoded_Str = {}
def convert_Number_to_unary_format_Str(q):
	str = ['1' for _ in range(q) ]
	str.append('0')
	return "".join(str)

def encode_Number_to_encoded_Str_List(S, K):
	m = pow(2, K)
	q = S // m
	r = S % m
	
	encoded_list = [ convert_Number_to_unary_format_Str(q), format(r, "b").zfill(K)]
	#print('original: ' + format(S, "b")  +  ' encoded: ' + "".join(encoded_list))
	return encoded_list

def encode_Number_to_encoded_Str(S, K):
	encoded_Str_List = encode_Number_to_encoded_Str_List(S, K)
	encoded_Str = "".join(encoded_Str_List)
	if encoded_Str in g_Dict_for_encoded_Str:
		prev_encoded_Str = encoded_Str
		encoded_Str = g_Dict_for_encoded_Str[prev_encoded_Str]
		if DEBUG_MODE:
			print('encoding in g_Dict')
			print(f'{prev_encoded_Str} -> {encoded_Str}')
	return encoded_Str

def encode_Number_List_to_encoded_Str(S_List, K):
	encoded_List = []
	for i, S in enumerate(S_List):
		encoded_List.append(encode_Number_to_encoded_Str(S, K))
		if DEBUG_MODE and i == 20:
			print(encoded_List)
	return "".join(encoded_List)


def generate_Number_List_to_encoded_Str_Dict(S_List, K):
	global g_Dict_for_encoded_Str
	g_Dict_for_encoded_Str = {}
	encoded_List = []

	for i, S in enumerate(S_List):
		encoded_List.append(encode_Number_to_encoded_Str(S, K))
		if DEBUG_MODE and i == 20:
			print(encoded_List)
	c = Counter(encoded_List)
	if DEBUG_MODE:
		print(c)
		print("-"*30)
	low_freq_short_len = []
	for k in sorted(c.keys()):
		element = c[k]
		if element < 3000 and len(k) < 40 // K:
			if DEBUG_MODE:
				print(f'{k}:{element}', end=", ")
				print(f'')
				print("="*30)

			low_freq_short_len.append(k)
	high_freq_long_len = []
	for k in sorted(c.keys(), reverse=True):
		element = c[k]
		if element > 10000 and len(k) > 40 // K:
			if DEBUG_MODE:
				print(f'{k}::{element}', end=", ")
				print(f'')
				print("-"*30)
			high_freq_long_len.append(k)
	for short_Str, long_Str in zip(low_freq_short_len, high_freq_long_len):
		g_Dict_for_encoded_Str[short_Str] = long_Str
		g_Dict_for_encoded_Str[long_Str] = short_Str

	if DEBUG_MODE:
		print('g_Dict_for_encoded_Str')
		print(g_Dict_for_encoded_Str)
		print(f'')

def encode_File_to_Unaligned_Str(filename, K):
	with open(filename, 'rb') as file:
		byteBuffer = bytearray(file.read())
	if DEBUG_MODE:
		for i, byte in enumerate(byteBuffer):
			if i < NUMBERS_TO_SHOW:
				print(f'byte[{i}]: {byte}')
		for i in range(NUMBERS_TO_SHOW):
			print(f'byte[{i-NUMBERS_TO_SHOW}]: {byteBuffer[i-NUMBERS_TO_SHOW]}')	

	generate_Number_List_to_encoded_Str_Dict(byteBuffer, K)
	return encode_Number_List_to_encoded_Str(byteBuffer, K)

def encode_File_to_File(source_filename, destination_filename, K):
	encoded_Str = encode_File_to_Unaligned_Str(source_filename, K)
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

	encoded_Byte_List = []
	for i in range(0, len(encoded_Str), 8):
		Element_as_Str = encoded_Str[i:i+8]
		Element_as_Byte = eval('0b' + encoded_Str[i:i+8])
		encoded_Byte_List.append(Element_as_Byte)
		if DEBUG_MODE:
			print(f'{Element_as_Str} {Element_as_Byte} {format(Element_as_Byte, "x")}')
	if DEBUG_MODE:
		for byte in bytearray(encoded_Byte_List):
			print(f'bytearray: {byte} {format(byte, "x")}')	
	if DEBUG_MODE:
		print(f'encoded Binary List: {encoded_Byte_List}')
		print(f'encoded Binary List: {bytearray(encoded_Byte_List)}')

	with open(destination_filename, 'wb') as binary_file:	
		binary_file.write( bytearray(encoded_Byte_List) )
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

def decode_to_Byte_List2(encoded_str, K):
	decoded_List = []
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

		if encoded_str[starting_index: q + 1 + K] in g_Dict_for_encoded_Str:
			original_Str = encoded_str[starting_index: q + 1 + K]
			new_Str = g_Dict_for_encoded_Str[original_Str]
			if DEBUG_MODE and len(encoded_str[starting_index: q + 1 + K]) > 20:
				print(f'decoding {encoded_str[starting_index: q + 1 + K]} =====> {new_Str}')
			new_q = new_Str.find('0')
			new_r_str = new_Str[new_q + 1:new_q + 1 + K]	
			new_r = eval('0b' + new_r_str)
			decoded_List.append( (new_q - 0) * m + new_r)
		else:
			r = eval('0b' + r_str)
			decoded_List.append( (q - starting_index) * m + r)
		
		starting_index = q + 1 + K 
	return decoded_List

def decode_File_to_File(source_filename, destination_filename, K):
	m = pow(2, K)
	with open(source_filename, 'rb') as file:
		byteBuffer = bytearray(file.read())
	if DEBUG_MODE:
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

	if DEBUG_MODE:
		print("making String finished")
	Byte_List = decode_to_Byte_List2(encoded_Str, K)

	if DEBUG_MODE:
		print(f'{Byte_List[:NUMBERS_TO_SHOW]}')
		print(f'{Byte_List[-NUMBERS_TO_SHOW:]}')

	with open(destination_filename, 'wb') as binary_file:
		binary_file.write( bytearray(Byte_List) )		
	
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

def generate_PKL_File(PKL_FILENAME):
	with open(pkl_filename, 'wb') as fp:
		pickle.dump(g_Dict_for_encoded_Str, fp)
	print(f'{original_wav_filename}, {K} pickle data {os.path.getsize(pkl_filename)}')

def retrieve_from_PKL_File(PKL_FILENAME):
	global g_Dict_for_encoded_Str
	with open(PKL_FILENAME, 'rb') as fp:
		g_Dict_for_encoded_Str = pickle.load(fp) 

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
#for original_wav_filename in ['Sound1.wav']:
	for K in [2, 4]:
#	for K in [2]:
		encoded_filename = original_wav_filename.split('.')[0] + '_Enc' + '.ex2'
		decoded_filename = original_wav_filename.split('.')[0] + '_EncDec' + '.wav' 
#		g_Dict_for_encoded_Str = {}
	
		encode_File_to_File(original_wav_filename, encoded_filename, K)
		pkl_filename = 'data.pkl'
#		with open(pkl_filename, 'wb') as fp:
#			pickle.dump(g_Dict_for_encoded_Str, fp)
		generate_PKL_File(pkl_filename)
#		print(f'{original_wav_filename}, {K} pickle data {os.path.getsize(pkl_filename)}')

		original_wav_filesize = os.path.getsize(original_wav_filename)
		encoded_file_filesize = os.path.getsize(encoded_filename)
		print(f'end Encoding {K}: {original_wav_filename} {original_wav_filesize}-> {encoded_filename} {encoded_file_filesize}')
#		with open(pkl_filename, 'rb') as fp:
#			g_Dict_for_encoded_Str = pickle.load(fp)
		retrieve_from_PKL_File(pkl_filename)
		decode_File_to_File(encoded_filename, decoded_filename, K)
		print('end Decoding')

		if compare_Binary_Files(original_wav_filename, decoded_filename):
			print(f'same files {original_wav_filename} {decoded_filename}')
		else:
			print(f'different files {original_wav_filename} {decoded_filename}')




