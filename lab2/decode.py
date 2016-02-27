import math 
import sys
import json

def get_tuple(nxt_str):

    offbit = ''
    lenbit = ''
    charbit = ''

    #get next tuple
    for bits in range(0, len(nxt_str)):

        if (bits < 10):
            offbit += nxt_str[bits]

        elif (bits >=10 and bits < 16):
            lenbit += nxt_str[bits]

        elif (bits >= 16):
           charbit += nxt_str[bits]


    offset = int(offbit, 2)
    length = int(lenbit, 2)
    char = chr(int(charbit, 2))

    return (offset, length, char)

            
def main():
    input_name = str(sys.argv[1])
    output_name = str(sys.argv[2])

    lenN = 1024
    lenM = 64

    search = ''
    look_ahead = ''
    output = ''


    file = open(input_name, "rb")


    try:

        bit = file.read(1)

        #decode file
        while (bit != ''):

            #get next tuple
            next_str = ''
            bits = 0

            #get 24-bit tuple
            while (bits < 24):

                if (bit == ''):
                    break

                next_str += bit
                bit = file.read(1)
                bits += 1

            offset, length, char = get_tuple(next_str)

            next_out = ''

            #decode
            if (length > 0):
                for i in range(0, length):
                    next_out += search[offset + i]
                    search += search[offset + i]

                next_out += char
                search += char

            else:
                next_out += char
                search += next_out

            output += next_out

            #shift window
            shift = (length + 1)

            if (len(search) > lenN):
                search = search[shift:]


    finally:
        file.close()


    with open(output_name, "w") as text_file:
        text_file.write(output)

if __name__ == '__main__':
    main()