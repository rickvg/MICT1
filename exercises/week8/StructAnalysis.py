from struct import *
import binascii
import re
from PIL import Image

#ImageHeader ZIF - definition:
magicValue = 4 #char
imageWidth = 4 #uint32
imageHeight = 4 #uint32
imageLength = 4 #uint32

#Chunk
chunkType = 4 #char
chunkLength = 4 #uint32
#chunkData depends on chunkLength

#Function definitions
def ReadChunk():
    strChunkType = unpack("<4s", file.read(chunkType))[0]
    intChunkLength = unpack("<I", file.read(chunkLength))[0]
    if intChunkLength > 0:
        strChunkData = file.read(intChunkLength)
    return strChunkType, intChunkLength, strChunkData


file = open("modified.zif", "rb")
content = file.read()

file.seek(0)

#Read header
strMagic = unpack("<4s", file.read(magicValue))
intWidth = unpack("<I", file.read(imageWidth))[0]
intHeight = unpack("<I", file.read(imageHeight))[0]
intLength = unpack("<I", file.read(imageLength))[0]

imgSize = (intWidth, intHeight)
arrChunkData = []
strImage = b""

while file.tell() < intLength:
    arrChunkData.append(ReadChunk())

for i in range(0,len(arrChunkData)):
    if arrChunkData[i][0] == b"COLR":
        hexString = arrChunkData[i][2]
        i = 0

        while i < len(hexString):
        #print(str(binascii.hexlify(hexString[i:i+4])))
            if not binascii.hexlify(hexString[i:i+4]).endswith(b"ff"):
                print(i)
                print("found anomaly")
            i = i + 4

for m in re.finditer(re.compile(re.escape(b"COLR")), content):
    offSetCOLR = m.start() + 8

#Read RGB data and output to file
f = open("imagedata.zif", "wb")
for m in re.finditer(re.compile(re.escape(b"DATA")), content):
    print("found")
    file.seek(m.start()+4)
    ChunkLen = unpack("<I", file.read(4))[0]
    p = 0
    while p < ChunkLen:
        intOffSet = unpack("<I",file.read(4))[0]
        valueFoundAt = offSetCOLR + (intOffSet * 4)
        currentPos = file.tell()
        file.seek(valueFoundAt)
	currentRGB = file.read(4)
	strImage += currentRGB
	f.write(currentRGB)
	file.seek(currentPos)
        
        p = p + 4
f.close()

#Save RGB data to image in format BGRA
img = Image.fromstring('RGBA', imgSize, strImage, 'raw', 'BGRA')
img.save("output.png")
               

