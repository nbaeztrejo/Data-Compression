import math 
import sys
import json
import hashlib

input_file = open("encoded.txt", "rb")

header = json.loads(input_file.readline())

huffman_code = json.loads(input_file.readline())
decode_dict = {v:k for k,v in huffman_code.iteritems()}

binary_data = input_file.readline()
binary_string = ""

while binary_data != "":
    binary_data = int(binary_data[:-1])
    binary_string += format(binary_data, '08b')
    binary_data = input_file.readline()

print "started decoding..."

decoded_data = ""
while len(decoded_data) != header['size']:
    sub_str = ""
    i = 0
    while sub_str not in decode_dict:
        sub_str = binary_string[0:i]
        i += 1
        
    decoded_data += chr(int(decode_dict[sub_str]))
    binary_string = binary_string[i-1:]


if hashlib.md5(decoded_data).hexdigest() == header['hash']:
    f = open("decoded.txt", "wb")
    f.write(decoded_data)

print "...done decoding"