import math 
import sys
import json

#based of given pseudocode
def LZ77_search(search, look_ahead):
    ls  = len(search)
    llh = len(look_ahead)

    if (ls == 0):
    #handle special case (same as no match found)
        return (0,0, look_ahead[0])
        

    if (llh == 0):
    #error condition, why would you call with empty look-ahead?
        return (0,0, '')

    best_offset = 0
    best_length = 0

    buf = search + look_ahead

    search_pointer = ls

    #all of the potential starting positions for search
    for i in range(0,ls): 
        offset = 0
        length = 0
        while (buf[i+length] == buf[search_pointer+length]):

            #found a match
            length += 1

            #check for search reaching the end of the look_ahead
            if (search_pointer + length == len(buf)):
                length -= 1
                break

        if (length > best_length):
            best_offset = i
            best_length = length

    return (best_offset, best_length, buf[search_pointer+best_length])


def main():
    input_name = str(sys.argv[1])
    output_name = str(sys.argv[2])

    #window doesn't move until after 1024
    lenN = 1024
    lenM = 64

    search = ''
    look_ahead = ''
    output = ''

    zerozero = bytes('0000000000000000')

    file = open(input_name, "rb")

    hi = 0

    try:

        bit = file.read(1)

        #fill look_ahead buffer
        while (len(look_ahead) < lenM):

            if (bit == ''):
                break

            look_ahead += bit
            bit = file.read(1)

            hi+=1
            


        while (len(search) < lenN):

            if (bit == ''):
                break
            
            charbit = format(ord(look_ahead[0]), 'b')
            while (8 - len(charbit) > 0):
                charbit = '0' + charbit
            

            next_out = zerozero + charbit
            output += bytes(next_out)
            #next_out = '{0,0,' + look_ahead[0] + '}'
            #print next_out
            #output += next_out
            search += look_ahead[0]
            look_ahead = look_ahead[1:] + bit
            bit = file.read(1)

            hi+=1
        
        #print search, look_ahead

        while (bit != '' or look_ahead != ''):

            #print LZ77_search(search, look_ahead)
            offset, length, char = LZ77_search(search, look_ahead)

            shift = length + 1
            search += look_ahead[:shift]
            search = search[shift:]

            look_ahead = look_ahead[shift:]

            if (shift > lenM):
            	shift = lenM

            while (shift > 0):

                if (bit == ''):
                    break

                look_ahead += bit
                bit = file.read(1)
                shift -= 1
                hi +=1

            
            charbit = format(ord(char), 'b')
            while (8 - len(charbit) > 0):
                charbit = '0' + charbit

            offbit = format(offset, 'b')
            while (10 - len(offbit) > 0):
                offbit = '0' + offbit

            lenbit = format(length, 'b')
            while (6 - len(lenbit) > 0):
                lenbit = '0' + lenbit 

            next_out = offbit + lenbit + charbit
            output += bytes(next_out)

            #next_out = '{' + str(offset) + ',' + str(length) + ',' + char + '}'
            #output += next_out



    finally:
        file.close()


    with open(output_name, "w") as text_file:
	    text_file.write(output)

if __name__ == '__main__':
	main()