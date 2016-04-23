import math 
import sys
import json
import hashlib

code_file = open("code.txt", "rb")
file = open(sys.argv[1], "rb")

code_dict = json.loads(code_file.readline())
code_file.close()

original_string = ""
binary_string = ""

print "started encoding..."

#convert file into encoded string
try:
    byte = file.read(1)
    while byte != "":
    	original_string += byte
    	index = str(ord(byte))
        binary_string += code_dict[index]
        byte = file.read(1)
finally:
    file.close()

print "...done encoding"

count = (8 - (len(binary_string) % 8))
for i in range(0,count):
    binary_string += "0"

outfile = open("encoded.txt", "wb")
out = {}
out['size'] = len(original_string)
out['hash'] = hashlib.md5(original_string).hexdigest()

outfile.write(json.dumps(out) +"\n" )
outfile.write(json.dumps(code_dict)+"\n" )

print "started writing..."

#convert encoded string to byte file
while (binary_string != ""):
	byte_string = ""
	for i in range(0,8):
		byte_string += binary_string[0]
		binary_string = binary_string[1:]
	outfile.write(str(int(byte_string,2)) + "\n")
	
outfile.close()

print "...done writing"

