#!/usr/bin/python3

from PIL import Image
import sys, array, binascii, argparse

'''
Function: decode

Programmer: Yiaoping Shu + Anthony 

Date: October 5 2018

Notes: This function takes the cover image in passed on by utility, then converts it to RGB, gaterhing the bits
from the last bits as encoded from stego. It takes those last bits and stores it for writing to a file that 
the user has named. Checks for delimiters to separate how large the file is and the separation between the bytes.

'''

def decode(cover, fileName):
	global messageSize
	global message
	global bitList

	bitList = ""
	messageSize = 0
	message = ""

	cover = Image.open("pictures/New/" + cover).convert('RGB')
	pixels = cover.load()
	width, height = cover.size
	messageSize = 208
	indexNumb = 0
	count = 0
	byte = ""
	byteList = []
	fileSize = ""
	delimiter = "00000000"

	for w in range(width):
		for h in range(height):
			red, green, blue = pixels[w,h]
			redPixels = bin(red)[2:].zfill(8)[7]
			greenPixels = bin(green)[2:].zfill(8)[7]
			bluePixels = bin(blue)[2:].zfill(8)[7]
			colourBitList = [redPixels, greenPixels, bluePixels]

			for i in range(len(colourBitList)):
				byte += colourBitList[i]
				if len(byte) == 8:
					byteList.append(byte)
					if byte == delimiter and count == 0:		#checks for first delimiter
						byteList = []
						count += 1
					elif byte == delimiter and count == 1:	#grabs the next bytes for file size
						messageSize = b''.join(binascii.unhexlify('%x' % int(b,2)) for b in byteList[0:len(byteList) - 1])
						byteList = []
						count += 1
						continue
					byte = ""

				if count == 2:
					if indexNumb < int(messageSize):
						bitList += colourBitList[i]
						indexNumb += 1
					else:
							for i in range(int(messageSize)-1):
								message += bitList[i]
							writeList = []

							for i in range (0, len(message)//8):
								writeList.append(int(message[i*8:(i+1) * 8], 2))

							fileByteList = array.array('B', writeList).tostring()
							dataToFile = bytearray(fileByteList)
							fileHandler = open("pictures/New/" + fileName, 'wb')
							fileHandler.write(dataToFile)
							print("Writing to file...")						
							return


