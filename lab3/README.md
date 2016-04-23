CS181 - Lab 3
November Baez Trejo
4/22/16

Run as python script:

For Part A:
Run as python huffman.py text_file.txt. 
The the JSON string containing the Huffman code will be output as code.txt

For Part B:
Run as python encode.py text_file.txt. 
The encoded result will be output as encoded.txt

For Part C:
Run as python decode.py. 
The decoded result is output as decoded.txt 

*Unfortunately, the encoding algorithm does not have good performance, so any file larger than 500KB will take more than 15 minutes to encode


Huffman
	20000 Leagues: -218%
	Hamlet: -212%
	Beowulf: -209%

LZ77
	20000 Leagues: -600%
	Hamlet: -670%
	Beowulf: -616%

Overall, it appears Huffman created smaller files than LZ77, but at the cost of performance.

