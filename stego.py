#!/usr/bin/python3

import sys, os, argparse, binascii, array
from PIL import Image

'''
Function: 	encode

Programmer: 	Yiaoping + Anthony 

Date:			October 3rd 2018

Notes: The purpose of this function is to take all the arguments from util, open up the files that was 
passed through, then take the secret file and read it. It takes the cover file and begins
writing to it, by taking the last bit from secret file's byte and swapping it in.
'''

def encode(cover, secret, fileName):
	totalBytes = ""
	delimiter = "00000000"
	binaryData = ""


	filename = os.path.basename(secret)

	totalBytes += delimiter

	with open("pictures/" + filename, 'rb') as myfile:
		data_byte_array = bytearray(myfile.read())

	for byte in data_byte_array:
		binaryData += bin(byte)[2:].zfill(8)

	size = list(str(len(binaryData)))
	fileSize = ''.join(format(ord(x), 'b').zfill(8) for x in size)
	fileSize += delimiter

	totalBytes += fileSize + binaryData

	cover = Image.open("pictures/" + cover).convert('RGB')
	pixels = cover.load()
	width, height = cover.size
	byteNumb = 0;
	lastBit = 0;

	for w in range(width):
		for h in range(height):
			red, green, blue = pixels[w,h]
			redP = list(bin(red)[2:].zfill(8))
			greenP = list(bin(green)[2:].zfill(8))
			blueP = list(bin(blue)[2:].zfill(8))
			rgbList = [redP, greenP, blueP]
			rgbDecimalVal = []

			if lastBit == 0:
				for rgbBitVal in rgbList:
					rgbBitVal[7] = totalBytes[byteNumb]
					byteNumb += 1
					rgbDecimalVal.append(int(''.join(str(e) for e in rgbBitVal), 2))
				pixels[w,h] = (rgbDecimalVal[0],rgbDecimalVal[1],rgbDecimalVal[2])

			if len(totalBytes) - byteNumb < 3:
				if lastBit == 0:
					lastBit = 1
					continue;
				else:
					rgbDecimalVal = [red,green,blue]
					for i in range(len(totalBytes) - byteNumb):
						rgbList[i][7] = totalBytes[byteNumb]
						rgbDecimalVal[i] = (int(''.join(str(e) for e in rgbList[i]), 2))
					pixels[w,h] = (rgbDecimalVal[0],rgbDecimalVal[1],rgbDecimalVal[2])
	cover.save("pictures/New/" + fileName)

