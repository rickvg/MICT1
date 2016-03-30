#Python version 3.4.3
#By: Groep 4 - Rick van Gorp, Nursize Bilen, Joeri van Grimbergen

import re
import binascii
import os
import sys

with open("ALLheaders.txt", "r") as f:
    arrHeaders = f.read().splitlines()
    
for i in range(0,len(arrHeaders)):
    arrHeaders[i] = binascii.unhexlify(arrHeaders[i])

print("Database with known Magic Values loaded:\n" + str(arrHeaders))

arrFiles = []

if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        arrFiles.append(str(sys.argv[i]))
else:
    arrFiles.append(str(input("\nPlease input a valid filename:\n")))


for i in range(0,len(arrFiles)):
    with open(arrFiles[i], "rb") as file:
        intLen = 0
        arrOutPutData = []
        while intLen < os.path.getsize(arrFiles[i]):
            content = file.read(16384) #Block = 16384 bytes
            intLen = intLen + 16384
            for k in range(0,len(arrHeaders)):
                for m in re.finditer(re.compile(re.escape(arrHeaders[k])), content):
                    arrOutPutData.append([hex(m.start()+intLen-16384),arrHeaders[k]])
                    print("\n" + hex(m.start()+intLen-16384))
                    print(arrHeaders[k])
        file.close()
    strOutputFile = "Results - " + arrFiles[i] + ".txt"
    with open(strOutputFile, "w") as fOutPut:
        fOutPut.write("Value\tLocation\n")
        for j in range(0,len(arrOutPutData)):
            fOutPut.write(str(arrOutPutData[j][1]) + "\t" + str(arrOutPutData[j][0]) + "\n")
        
