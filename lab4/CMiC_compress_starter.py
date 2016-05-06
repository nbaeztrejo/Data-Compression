'''
CMiC Image Compressor

November Baez, Brenda Garcia, Jane Kang

EXTRA CREDIT: color pictures, odd dimensions
'''

#CMiC Image Compressor Starter file
#first some imports
import sys
import scipy
import scipy.ndimage
import numpy as np
import PIL
from PIL import Image
import pywt
import argparse
import operator 
import sys, os
import json

# import cv2
from heapq import merge
import hashlib
import struct

#wrapper for showing np.array() as an image
def show(image):
	scipy.misc.toimage(image).show()

# Compresses an image file using sub-band decomposition, differential coding, quantization, and Huffman coding
# @return the compressed file with image metadata, Huffman code dictionary, and encoded binary data
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_image")
	parser.add_argument("output_file")
	parser.add_argument("--wavelet", help="wavelet name to use. Default=haar", default="haar")
	parser.add_argument("--quantize", help="quantization level to use. Default=4", type=int, default=4)
	args = parser.parse_args()

	input_file_name = args.input_image
	try:
		im = scipy.ndimage.imread(input_file_name, flatten=False, mode="RGB")
		print "Attempting to open %s..." % input_file_name
	except:
		print "Unable to open input image. Qutting."
		quit()
	show(im)

	(height, width, channel) = im.shape
	print "Image height:", height
	print "Image width:", width
	wavelet = args.wavelet
	q = args.quantize

	r, g, b = splitRGB(im)
	
	# Add a row and/or column of black pixels if odd dimension
	if (height%2 == 1):
		r = np.vstack([r, [0]*width])
		g = np.vstack([g, [0]*width])
		b = np.vstack([b, [0]*width])

	if (width%2 == 1):
		addCol = np.zeros((r.shape[0], width+1))
		addCol[:,:-1] = r
		r = addCol

		addCol = np.zeros((g.shape[0], width+1))
		addCol[:,:-1] = g
		g = addCol

		addCol = np.zeros((b.shape[0], width+1))
		addCol[:,:-1] = b
		b = addCol

	# Sub-band decomposition, differential encoding, quantization
	list_concat_R = im_processing(r, wavelet, q, width, height)
	list_concat_G = im_processing(g, wavelet, q, width, height)
	list_concat_B = im_processing(b, wavelet, q, width, height)
	list_concat = list_concat_R + list_concat_G + list_concat_B

	# Huffman encoding
	d_counter = freq(list_concat)
	d_items = d_counter.items()
	tree = create_bin_tree(d_items)
	code = []
	huff(tree, "", code)
	codes_ = dict(code)
	bin_str = encode_huffman(list_concat, codes_)

	# Write the compressed file
	with open('bincompressedfile.bin', 'wb') as f:
		json_header = {'height': height, 'width':width, "list_len": len(list_concat_B),
			"wavelet":wavelet, "q":q}
		f.write(json.dumps(json_header) + '\n')
		f.write(json.dumps(codes_) + '\n')
		f.write(binStr_to_bin(bin_str))
	

# Split the 3D array by color channels to produce 3 2D arrays
# @param im - 3D numpy array of pixels
# @return 2D array for red, green, blue
def splitRGB(im):
	image_fromArray = Image.fromarray(im)
	r, g, b = image_fromArray.split()
	red = np.array(r)
	green = np.array(g)
	blue = np.array(b)
	return (red, green, blue)

# Sub-band decomposition, differential coding, quantization
# @return flattened and processed 2D arrays concatenated in order (1D array)
# @param im - 2D numpy array of pixels
# @param wavelet - wavelet to use in sub-band decomposition
# @param q - quantization step size
# @param width - image width
# @param height - image height
def im_processing(im, wavelet, q, width, height):
	# Sub-band decomposition
	# Available wavelets: Haar (haar) Daubechies (db) Symlets (sym) Coiflets (coif)
	LL, (LH, HL, HH) = pywt.dwt2(im, wavelet=wavelet, mode='periodization') 

	# Differential coding, add 0 to prevent offset by first pixel value
	flat_LL = LL.flatten()
	LL_array = np.array(flat_LL)
	LL_cast = np.round(LL_array).astype(int)
	LL_wzero = np.insert(LL_cast, 0, 0)
	LL_diff_array = np.diff(LL_wzero)
	LL_py = LL_diff_array.tolist()

	# Quantization
	HL_q = HL.flatten()/q
	LH_q = LH.flatten()/q
	HH_q = HH.flatten()/q

	HL_cast = np.round(HL_q).astype(int)
	LH_cast = np.round(LH_q).astype(int)
	HH_cast = np.round(HH_q).astype(int)

	HL_py = HL_cast.tolist()
	LH_py = LH_cast.tolist()
	HH_py = HH_cast.tolist()

	list_concat = LL_py + LH_py + HL_py + HH_py

	#the following block of code will let you look at the decomposed image. Uncomment it if you'd like
	'''dwt = np.zeros((height, width))
	dwt[0:height/2, 0:width/2] = LL
	dwt[height/2:,0:width/2] = HL
	dwt[0:height/2, width/2:] = LH
	dwt[height/2:,width/2:] = HH
	show(dwt)'''

	return list_concat


# Creates Huffman code for pixel values
# @param binTree - binary tree of pixel value frequencies
# @param partialCode - partially constructed Huffman code, empty string as default
# @param codeList - list of (pixel, Huffman code) tuples
def huff(binTree, partialCode, codeList):
	if isinstance(binTree, int):
		codeList.append((binTree, partialCode))
	else:
		left = huff(binTree[0], partialCode + "0", codeList)
		right = huff(binTree[1], partialCode + "1", codeList)


# Calculate frequency of each pixel value
# @return pixel frequency dictionary
# @param im - flattened 1D array of pixels
def freq(im):
	freqDict = dict()
	for item in im:
		if item not in freqDict:
			freqDict[item] = 1
		else:
			freqDict[item] += 1

	return freqDict


# @return the binary tree out of pixel frequencies
# @param d_items - list of pixel frequency tuples
def create_bin_tree(d_items):
	lst = sorted(d_items, key=lambda y:y[1])

	while len(lst) > 1:
		z = lst[0]
		y = lst[1]
		v = z[1] + y[1]
		k = [z[0], y[0]]
		lst = lst[2:]+[(k,v)]
		lst = sorted(lst, key=lambda y:y[1])

	return lst[0][0]


# Huffman encode the pixels
# @return encoded binary string
# @param im - flattened 1D array of pixels
# @oaran huff_dict - Huffman code dictionary
def encode_huffman(im, huff_dict):
	binst = ""
	for item in im:
		bin_val = huff_dict[item]
		binst += bin_val

	# Pad the string to make its length a multiple of 8
	padd_needed = 8 - (len(binst) % 8) 
	while padd_needed > 0:
		binst += "0"
		padd_needed -= 1

	return binst


# Convert binary string into binary data
# @return binary data, each bit representing 0 or 1
# @param input - binary string, made of 0s and 1s
def binStr_to_bin(input):
	binary = ""
	for i in range(0, len(input)/8):
		bits = input[i*8:i*8+8]
		b = 0 
		powers = range (0,8)
		powers.reverse()
		for i in range(len(bits)):
			b += int(bits[i]) * pow(2, powers[i])
		binary += struct.pack("B", b)
	return binary


if __name__ == '__main__':
	main()