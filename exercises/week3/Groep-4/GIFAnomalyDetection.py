#Python version 3.4.3
#By: Groep 4 - Rick van Gorp, Nursize Bilen, Joeri van Grimbergen

from struct import *
import sys
import os
import binascii
import re
import random

#Application header: 21FF0B

#GIF Header definitie
intDefinition = 6 #Signature + Version = Length 6 Bytes

#Logical screen descriptor chunk
#Should be read as little endian
intWidth = 2
intHeight = 2
intPacked = 1
intBackgroundColorandAspect = 2

#Function for finding left boundary for specific data block
def CheckBlockLeft(f, currentPos, strBinary):
    blnEndOfData = False
    count = 1
    while blnEndOfData == False:
        f.seek(currentPos - count)
        if file.read(1) == strBinary:
            count = count + 1
        else:
            blnEndOfData = True
            if count == 1:
                return False
            else:            
                return (f.tell()-1)

#Function for finding right boundary for specific data block
def CheckBlockRight(f, currentPos, strBinary):
    currentPos = f.tell()
    blnEndOfData = False
    count = 1
    while blnEndOfData == False:
        f.seek(currentPos + count)
        if file.read(1) == strBinary:
            count = count + 1
        else:
            blnEndOfData = True
            if count == 1:
                return False
            else:            
                return (f.tell()-1)

#Function to check the validity of the image descriptor block           
def CheckIMGDescriptor(f, currentPos, MaxWidth, MaxHeight):
    f.seek(currentPos)
    f.read(5)
    arrWrongBoundaries = []
    intWidth = unpack("<H",f.read(2))[0]
    intHeight = unpack("<H", f.read(2))[0]
    if (intWidth > MaxWidth or intHeight > MaxHeight) or (intWidth == 0 and intHeight == 0):
        return 0, f.tell(), arrWrongBoundaries
    intPacked = str(bin(unpack("<B", f.read(1))[0]))
    arrPacked = list(intPacked[2:len(intPacked)])
    if arrPacked[0] == "1":
        intColorTable = int(intPacked[len(intPacked)-3:len(intPacked)],2)
        intSizeLocalColor = 3*2**(intColorTable+1)
        LocalColor = f.read(intSizeLocalColor)
    f.read(1)
    blnTerminated = False
    count = 0
    arrDBSize = [] #Used to define biggest size used, mostly only a few blocks differ from this
    while blnTerminated == False:
        blockPos = f.tell()
        intDBSize = unpack("B", f.read(1))[0]
        if intDBSize <= 255 and intDBSize > 0: #It is very unlikely for image data to be 0.
            f.read(intDBSize)
            arrDBSize.append(intDBSize)
            if intDBSize < max(arrDBSize):
                arrWrongBoundaries.append(blockPos)
                arrWrongBoundaries.append(f.tell())
            intBlockTerm = unpack("B", f.read(1))[0]
            if intBlockTerm == 0:
                blnTerminated = True
                return 2, f.tell(), arrWrongBoundaries
            else:
                f.seek(f.tell()-1)
        else:
            return 2, f.tell(), arrWrongBoundaries

#Function to check the validity of the Application Extension header               
def CheckApplicChunk(f, currentPos):
    f.seek(currentPos+2)
    intBlockSize = unpack("B", f.read(1))[0]
    f.read(11)
    intDBSize = unpack("B", f.read(1))[0]
    strData = f.read(intDBSize)
    intBlockTerm = unpack("B", f.read(1))[0]
    if intBlockSize == 11 and intBlockTerm == 0:
        return 2, f.tell()
    else:
        return 0, f.tell()

#Function to check the validity of the Plain Text Extension header             
def CheckPlainChunk(f, currentPos):
    f.seek(currentPos+2)
    intBlockSize = unpack("B", f.read(1))[0]
    f.read(13)
    intDBSize = unpack("B", f.read(1))[0]
    strData = f.read(intDBSize)
    intBlockTerm = unpack("B", f.read(1))[0]
    if intBlockSize == 12 and intBlockTerm == 0:
        return 2, f.tell()
    else:
        return 0, f.tell()

#Function to check the validity of the Graphic Control Extension header               
def CheckGraphicChunk(f, currentPos):
    f.seek(currentPos+2)
    intBlockSize = unpack("B", f.read(1))[0]
    strPacked = str(bin(unpack("<B", f.read(1))[0]))
    intDelay = unpack("<H", f.read(2))[0]
    intColor = unpack("B", f.read(1))[0]
    intBlockTerm = unpack("B", f.read(1))[0]
    if intBlockSize == 4 and intBlockTerm == 0:
        return 2, f.tell()
    else:
        return 0, f.tell()

#Function to check the validity of the Comment Extension header           
def CheckCommentChunk(f, currentPos):
    f.seek(currentPos+2)
    intDBSize = unpack("B", f.read(1))[0]
    strData = f.read(intDBSize)
    intBlockTerm = unpack("B", f.read(1))[0]
    if intBlockTerm == 0:
        return False, f.tell()
    else:
        return False, f.tell()

blnSolved = False
arrNew = []

while blnSolved == False:
    file = open("f_z.data", "rb")
    content = file.read()

    file.seek(0)
    magic_val = file.read(6)
    strWidth = unpack("<H",file.read(2))[0]
    strHeight = unpack("<H",file.read(2))[0]

    arrKnownValues = [["APPLIC", b"\x21\xff"],["GRAPHIC",b"\x21\xf9"],["COMMENT",b"\x21\xfe"],["PLAIN",b"\x21\x01"],["IMG", b"\x00\x2c"],["TRAILER",b"\x3b"]]
    arrPossibleValues =[]
    arrVerifiedValues = []
    arrBrokenValues = []
    arrUnallocated = []
    arrDataBlockBounds = []
    
    #Determine possible locations of specific headers
    for i in range(0,len(arrKnownValues)):
        for m in re.finditer(arrKnownValues[i][1],content):
            arrPossibleValues.append([arrKnownValues[i][0],m.start()])

    #Take action based on the found data
    for i in range(0,len(arrPossibleValues)):
        if arrPossibleValues[i][0] == "APPLIC":
            test = CheckApplicChunk(file, arrPossibleValues[i][1])
            if test[0] != 0:
                # = Application block
                arrVerifiedValues.append([arrPossibleValues[i][0], arrPossibleValues[i][1], test[1]])
        elif arrPossibleValues[i][0] == "GRAPHIC":
            test = CheckGraphicChunk(file, arrPossibleValues[i][1])
            if test[0] != 0:
                # = Graphic Control Extension
                arrVerifiedValues.append([arrPossibleValues[i][0], arrPossibleValues[i][1], test[1]])
        elif arrPossibleValues[i][0] == "COMMENT":
            test = CheckCommentChunk(file, arrPossibleValues[i][1])
            if test[0] != 0:
                # = Comment Extension
                arrVerifiedValues.append([arrPossibleValues[i][0], arrPossibleValues[i][1], test[1]])
        elif arrPossibleValues[i][0] == "PLAIN":
            test = CheckPlainChunk(file, arrPossibleValues[i][1])
            if test[0] != 0:
                # = Plain Text Extension
                arrVerifiedValues.append([arrPossibleValues[i][0], arrPossibleValues[i][1], test[1]])
        elif arrPossibleValues[i][0] == "IMG":
            arrPossibleValues[i][1] = arrPossibleValues[i][1] + 1
            test = CheckIMGDescriptor(file, arrPossibleValues[i][1], strWidth, strHeight)
            if test[0] == 1:
                # = Broken Image Descriptor
                arrBrokenValues.append(arrPossibleValues[i])
            elif test[0] == 2:
                # = Image Descriptor
                arrVerifiedValues.append([arrPossibleValues[i][0], arrPossibleValues[i][1], test[1]])

            
            if isinstance(test[2], list):
                if len(test[2]) > 5:
                    i = 1
                    while i < len(test[2])-1:
                        if test[2][i+1]-test[2][i] > 0:
                            arrDataBlockBounds.append([test[2][i],test[2][i+1]])
                        i = i + 2
                              
    arrVerifiedValues = sorted(arrVerifiedValues, key=lambda x: x[2])
    print("Verified Values:\n" + str(arrVerifiedValues))
    
    #Find out unallocated spaces
    for i in range(0,len(arrVerifiedValues)-1):
        if (int(arrVerifiedValues[i+1][1]) - int(arrVerifiedValues[i][2])) > 0:
            arrUnallocated.append([arrVerifiedValues[i][2], arrVerifiedValues[i+1][1]])     
    print("\nUnallocated spaces (Boundaries):\n" + str(arrUnallocated))
    print("\nBroken Values (Boundaries):\n" + str(arrBrokenValues))
    print("\nProblems found in IMG Blocks:\n" + str(arrDataBlockBounds))
    if not arrUnallocated and not arrBrokenValues and not arrDataBlockBounds:
        blnSolved = True
    #elif arrNew:
        #if arrBrokenValues:
        #    strResult = Reorder(file, arrNew, brokenVal = arrBrokenValues)
        #else:
        #    strResult = Reorder(file,arrNew)
        #file.close()
        #file = open("e_r.data", "r+b")
        #file.seek(arrNew[0])
        #file.write(strResult)
        #file.close()
    else:
        #Search for same character (filled with zeroes) and determine blocks
        arrSameChar = []
        for i in range(0,len(arrUnallocated)):
            file.seek(arrUnallocated[i][0])
            strTest = file.read(1)
            blnEndOfBlock = False
            count = 0
            while blnEndOfBlock == False:
                intLeftPos = CheckBlockLeft(file, arrUnallocated[i][0] + count, strTest)
                if intLeftPos != False:
                    intRightPos = CheckBlockRight(file, arrUnallocated[i][0] + count, strTest)
                    if intRightPos != False:
                        if [intLeftPos,intRightPos] not in arrSameChar:
                            arrSameChar.append([intLeftPos,intRightPos])
                count=count+10000 #check with steps of 10000 whether there is another block with same value in the same unallocated block
                if count > (300000):
                    blnEndOfBlock = True

        #If blocks with same character found, continue to write edited data to file           
        if arrSameChar != []:
            file.seek(0)
            strFileSize = os.path.getsize("f_z.data")
            data = file.read(arrSameChar[0][0]+1)
            arrBlockMarkers = []
            if len(arrSameChar)==1:
                file.seek(arrSameChar[0][1])
            else:
                for i in range(0,len(arrSameChar)-1):
                    file.seek(arrSameChar[i][1])
                    data = data + file.read(arrSameChar[i+1][0]-(arrSameChar[i][1]-1))
                    arrBlockMarkers.append(arrSameChar[i+1][0]-(arrSameChar[i][1]-1))
            arrNew.append(arrSameChar[0][0])
            for i in range(0,len(arrBlockMarkers)):
                arrNew.append(arrNew[i] + arrBlockMarkers[i])
            print("\nMore specific unallocated spaces: " + str(arrSameChar))
            print("Above spaces are filled by: " + str(strTest))
            print("\nStart of block: " + str(arrNew))
            
            try:
                file.seek(arrSameChar[len(arrSameChar)-1][1])
                data = data + file.read(strFileSize)
            except:
                print("EOF")
            file.close()
            f = open("f_z.data", "wb")
            f.write(data)
            f.close()
            file.close()
        x = input("\nPress Enter to check again...")


