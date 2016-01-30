import math 
import sys
import json

name = str(sys.argv[1])

file = open(name, "rb")
bytes = {}
total = 0

try:
    byte = file.read(1)
    while byte != "":

    	total += 1
        
        if bytes.get(byte) is None:
            bytes[byte] = 1
        else:
            bytes[byte] += 1;
        byte = file.read(1)

finally:
    file.close()

chars = {}

ent = 0.

for key in bytes: 
    prob = float (bytes[key]) / float (total)
    ent = ent + prob * math.log(prob, 2)

    #not printable
    if ord(key) < 32 or ord(key) >= 127:
        chars[hex(ord(key))] = bytes[key]

    #printable
    else:
        chars[key] = bytes[key]

ent = -ent

chars["Total"] = total

print json.dumps({"Entropy": ent})
print json.dumps(chars, sort_keys=True)
