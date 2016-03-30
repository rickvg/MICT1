#Python version 3.4.3
#By: Groep 4 - Rick van Gorp, Nursize Bilen, Joeri van Grimbergen

import binascii
import os

file = open("x", "rb")
t = os.path.getsize("x")

file.seek(4)

byteFile = b""
pngSig = binascii.unhexlify("89504e47")
byteFile = byteFile + pngSig

while file.tell() < t:
    try:
       byteFirst =  file.read(1)
       byteSecond = file.read(1)
       byteFile = byteFile + byteSecond + byteFirst
    except:
        print("EOF")
        
f = open("t.png", "wb")
f.write(byteFile)
f.close()

