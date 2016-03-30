#Python version 3.4.3
#By: rickvg - https://github.com/rickvg

from struct import *

#PNG Header definition
intDefinition = 8 #Length of PNG identifier = 8 bytes

#PNG Chunk definition
intLength = 4       #Length of PNG chunk length identifier = 4 bytes
intChunkType = 4    #Length of PNG chunk type = 4 bytes
intChunkData = 0    #Depends on intLength
intCRC = 4          #Length of CRC = 4 bytes

#Function to read file by pre-defined chunks
def ReadChunk(f):
    offset = hex(f.tell()) #Get current location in file
    intLchunk = f.read(intLength)
    intLchunk = unpack('>I', intLchunk)[0] #Read as Big Endian -> Unsigned Integer
    strType = f.read(intChunkType)
    strChunkData = f.read(intLchunk)
    intChecksum = f.read(intCRC)
    intChecksum = unpack('>I', intChecksum)[0] #Read as Big Endian -> Unsigned Integer
    return [strType, intLchunk, offset]

#Count most common values to determine general size used per chunk data type
def FindMostCommon(chunkType):
    counter = {}
    for i in range(0,len(arrValues)):
        if arrValues[i][0] == chunkType:
            counter[arrValues[i][1]] = counter.get(arrValues[i][1], 0) + 1
    counts = [(j,i) for i,j in counter.items()]
    if counts:
        intMostCommon = max(counts)[1]
        return(intMostCommon)

#Print anomalies in length per chunk type
def PrintAnomalyCount(chunkType):
    intMostCommon = FindMostCommon(chunkType)
    for i in range(0,len(arrValues)):
        if arrValues[i][0] == chunkType:
            if arrValues[i][1] != intMostCommon and arrValues[i][1] != 0:
                print("Found anomaly in lenghts of: " + str(arrValues[i][0]))
                print("Explanation: It differs from the most used chunk length " + str(intMostCommon))
                print("Length found:" + str(arrValues[i][1]) +"\n")

newfile = open("t.png", 'rb')

magic_val = newfile.read(8)

arrDefaultPNG = [b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"iCCP", b"tEXt", b"zTXt", b"iTXt", b"bKGD", b"pHYs", b"sBIT", b"sPLT", b"hIST", b"tIME"]

#Read complete file until end
blnEOF = False
arrValues = []

while blnEOF == False:
    try:
        arrValues.append(ReadChunk(newfile))
    except:
        blnEOF = True

for i in range(0,len(arrDefaultPNG)):
    PrintAnomalyCount(arrDefaultPNG[i])

#Check if anomaly in Chunk Type exists
for i in range(0,len(arrValues)):
    if ((arrValues[i][0]) not in arrDefaultPNG): 
        print("Found anomaly for Chunk Type used in PNG-file:\n")
        print("Chunk Type:\tChunk Length\tChunk Offset")
        print(str(arrValues[i][0]) + "\t\t" + str(arrValues[i][1]) + "\t\t" + str(arrValues[i][2]))




