import re
import binascii

file = open("data", "rb")
content = file.read()

with open("ALLheaders.txt", "r") as f:
    arrHeaders = f.read().splitlines()
    
for i in range(0,len(arrHeaders)):
    arrHeaders[i] = binascii.unhexlify(arrHeaders[i])

print("Database with known Magic Values loaded:\n" + str(arrHeaders))

for i in range(0,len(arrHeaders)):
    for m in re.finditer(re.compile(re.escape(arrHeaders[i])), content):
        print("\n" + hex(m.start()))
        print(arrHeaders[i])
