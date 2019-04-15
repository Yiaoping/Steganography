#!/usr/bin/python3

import sys, os, argparse, binascii, array
from PIL import Image
from stego import encode
from image import decode

'''
Function: 	encode

Programmer: 	Yiaoping

Date:			October 2rd 2018

Notes: The purpose of this file is to process all user arguments and check whether
user wants to encode or decode the image(s). If user has chosen encoding, it will 
start encoding through the encoding function in the stego file. If user has selected
decode, it will start decoding the image through the image file.
'''

parser = argparse.ArgumentParser(description='Steganography')
parser.add_argument('-m', dest='mode')
parser.add_argument('-c', dest='cover')
parser.add_argument('-s', dest='secret')
parser.add_argument('-n', dest='fileName')
args = parser.parse_args()

def main():
	if args.mode == "encode":
		encode(args.cover, args.secret, args.fileName)
		print("finished encoding")

	elif args.mode == "decode":
		print("Starting to decode")
		decode(args.cover, args.fileName)
		print("Finished decoding")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print
