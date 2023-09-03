#                       !!
# 1111 1000  1011 1101  0011 1110  0110 1111 00110111111000001111010100111100000111110011111110000100
# 1111 1000  1011 1101    11 1110   110 1111  11011111100000111101011111001111111111110000100
# 0xf8       0xbd       0x3e       0x6f

import sys

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
	return "".join(encoded_List)

def encode_File_to_Str(filename, K):
	with open(filename, 'rb') as file:
		byteBuffer = bytearray(file.read())
	for i, byte in enumerate(byteBuffer):
		if i < NUMBERS_TO_SHOW:
			print(f'byte[{i}]: {byte}')
	for i in range(5):
		print(f'byte[{i-5}]: {byteBuffer[i-5]}')
	
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
		encoded_Str = encoded_Str.ljust(new_Len, '0')
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
		if starting_index + 1 + K >= Len_Str:
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
#		if q < 0:
#			print("???")
#			break
		starting_index = q + 1 + K
		#print(f'{starting_index}', end=" ")
#	print(f'encoded_Str: {encoded_Str} / Length {len(encoded_Str)}')	

	print("making string finished")
	result_List = []
	decode_to_List(encoded_Str, K, result_List)
	print(f'{result_List[:NUMBERS_TO_SHOW]}')
	print(f'{result_List[-5:]}')

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
		print('two files are different')
		return False
	for byte0, byte1 in zip(byteArray0, byteArray1):
		if byte0 != byte1:
			print(f'two files are different {byte0} {byte1}')
			return False
	return True


S0 = 0b00010011
S1 = 0b00010011
K = 4
S2 = 0b0001001100010011
S3 = 0b0001
S4 = 0b0011
S5 = 0b11111111

original_wave_filename0 = 'Sound1.wav'
original_wave_filename1 = 'Sound2.wav'

encoded_filename = 'new.hex'
decoded_filename = 'old.wav'

for original_wav_filename in ['Sound1.wav', 'Sound2.wav']:
	encode_File_to_File(original_wave_filename0, encoded_filename, K)
	print('end Encoding')
	decode_File_to_File(encoded_filename, decoded_filename, K)
	print('end Decoding')

	if compare_Binary_Files(original_wave_filename0, decoded_filename):
		print('same files')
	else:
		print('different files')




