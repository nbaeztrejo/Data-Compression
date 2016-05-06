'''
CMiC Image Decompressor

November Baez, Brenda Garcia, Jane Kang

EXTRA CREDIT: color pictures, odd dimensions
'''

#CMiC Reference Decoder
#CMiC Image Compressor Starter file
#first some imports
import sys
import scipy
import scipy.ndimage
import numpy as np
import PIL
from PIL import Image
import pywt
from collections import Counter
from heapq import merge
import re
import struct
import itertools
import json
import os

#wrapper for showing np.array() as an image
def show(image):
	scipy.misc.toimage(image).show()


# Decompress a CMiC compressed image file
# Undo sub-band decomposition, differential coding, Huffman coding
# @post output file contains the decompressed image
def main():
	try:
		input_file_name = sys.argv[1]
		print "Attempting to open %s..." % input_file_name
		input_file = open(sys.argv[1], 'rb')
	except:
		print "Unable to open input file. Qutting."
		quit()

	try:
		output_file_name = sys.argv[2]
		print "Attempting to open %s..." % output_file_name
		output_file = open(sys.argv[2], 'wb')
	except:
		print "Unable to open output file. Qutting."
		quit()

	header = json.loads(input_file.readline())
	huffCode = json.loads(input_file.readline())
	print "CMiC compression information:", header

	height = int(header['height'])
	width = int(header['width'])
	list_len = int(header['list_len'])
	wavelet = header['wavelet']
	q = int(header['q'])
	huff_dict = {v.encode() : k for k, v in huffCode.iteritems()}

	print "Parsing encoded data..."
	binary_data = input_file.read()
	binary_string = ""
	for byte in binary_data:
		binary_string += format(ord(byte),'08b')
	
	# Arbitrary height and width to handle decompressing odd dimension images
	iterHeight = height+1 if height%2 == 1 else height 
	iterWidth = width+1 if width%2 == 1 else width
	
	print "Huffman decoding encoded data..."
	decoded_data = []
	while len(decoded_data) != 3*4*(0.5*iterHeight * 0.5*iterWidth):
		sub_str = ""
		i = 0

		while sub_str not in huff_dict:
			sub_str = binary_string[0:i]
			i=i+1
		
		decoded_data += [int(huff_dict[sub_str])]
		binary_string = binary_string[i-1:]
		
	print "Splitting decoded data into RGB channels"
	rgb = []
	while (len(decoded_data) >= list_len):
		chan = decoded_data[:list_len]
		decoded_data = decoded_data[list_len:]
		rgb.append(chan)

	# Merge the color channels after undoing sub-band decomposition
	red_im = Image.fromarray(build_im(rgb[0], iterHeight, iterWidth, wavelet,q)).convert('L')
	green_im = Image.fromarray(build_im(rgb[1], iterHeight, iterWidth, wavelet,q)).convert('L')
	blue_im = Image.fromarray(build_im(rgb[2], iterHeight, iterWidth, wavelet,q)).convert('L')
	rgb = Image.merge("RGB", (red_im, green_im, blue_im))
	im = np.array(rgb)

	# If odd dimension, remove extra row and/or column of black pixels
	if height != im.shape[0]:
		im = np.delete(im, (height), axis=0)
	if width != im.shape[1]:
		im = np.delete(im, (width), axis=1)

	scipy.misc.toimage(im).save(output_file)


# Undo sub-band decomposition
# @return reconstructed 2D array of pixels
# @param decoded_data - 1D array of quantized pixels
# @param height - image height
# @param width - image width
# @param wavelet - wavelet used for sub-band decomposition
# @param q - quantization step size
def build_im(decoded_data, height, width, wavelet, q):
	LL = (np.cumsum(np.array(decoded_data[0:int(height/2 * width/2)]))).reshape(height/2, width/2)
	LH = (np.array(decoded_data[int(height/2 * width/2):2*int(height/2 * width/2)])*q).reshape(height/2, width/2)
	HL = (np.array(decoded_data[2*int(height/2 * width/2):3*int(height/2 * width/2)])*q).reshape(height/2, width/2)
	HH = (np.array(decoded_data[3*int(height/2 * width/2):4*int(height/2 * width/2)])*q).reshape(height/2, width/2)
	
	im = pywt.idwt2( (LL, (LH, HL, HH)), wavelet,mode='periodization' )
	show(im)
	return im


if __name__ == '__main__':
	main()