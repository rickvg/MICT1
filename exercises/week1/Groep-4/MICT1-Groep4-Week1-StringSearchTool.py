#Python versie 3.4.3
#By: Groep 4 - Joeri van Grimbergen, Nursize Bilen & Rick van Gorp
#u"\U0001F4A9"' = Pile of Poo

#Native Imports
import sys
import re
import base64
import binascii

print("Default encoding: " + sys.getdefaultencoding())

#Bestand met data lezen in binary mode
with open("week1.data", "rb") as f:
    content = f.read()

blnValidChoice = False

#Keuzemenu - Controle op valide keuzes
while blnValidChoice == False:
    print("1. Search for Base64 String (Plaintext input)\n2. Search by Unicode String\n3. Search by string\n")
    intChoice = input("\nMake a choice:\n")

    #Op basis van keuze voor Base64 -> Karakters encoderen en string van maken ipv bytes
    if intChoice == "1":
        strChar = input("Enter string (FORMAT: Plaintext, geen Base64):\n")
        print("\nProcessing request... This could take a while due to the amount of encoding methods in codecs.txt")
        blnValidChoice = True
    elif intChoice == "2":
        #Op basis van keuze voor Unicode -> Ingevoerde string omzetten naar ASCII-bytestring en een Unicode "u" voor plaatsen.
        strChar = input("Enter string (FORMAT: \\U0001F4A9):\n")
        strChar = str(bytes(strChar, 'ascii').decode('unicode-escape'))
        blnValidChoice = True
    elif intChoice == "3":
        strChar = input("Enter string:\n")
        blnValidChoice = True
    else:
        print("Invalid choice. Please choose by number\n")
    
#Array om records te verwijderen waarbij encoding fout aangeeft
toRemove = []

#Open bestand met encoding-formaten die verwerkt moeten worden
with open("codecs.txt", "r") as file:
    arrEncoding = file.readlines()

arrFound = []
arrIndex = []

intLength = 0

#Proberen om string te encoden met het opgegeven encodingsformaat
for i in range(0, len(arrEncoding)):
    arrFound2 = []
    arrtest = []
    if i != len(arrEncoding)-1:
        arrEncoding[i] = arrEncoding[i][0:len(arrEncoding[i])-1]
    try:
        setExist = set()
        #Encoderen van Base64 (bij Choice 1) volgens alle mogelijke encoderingsmethoden
        if intChoice == "1":
            newChar = str(base64.b64encode(strChar.encode(arrEncoding[i])))
            newChar = newChar[2:len(newChar)-1]
            for j in range(0,len(arrEncoding)):
                try:
                    #Zoeken van geëncodeerde binary string in data van bestand o.b.v. regex
                    for m in re.finditer(re.compile(newChar.encode(arrEncoding[j])), content):
                        if hex(m.start()) not in setExist:
                            arrFound2.append(hex(m.start()))
                            setExist.add(hex(m.start()))
                except:
                    test = 1
        else:
            #Zoeken van geëncodeerde binary string in data van bestand o.b.v. regex
            for m in re.finditer(re.compile(strChar.encode(arrEncoding[i])), content):
                arrFound2.append(hex(m.start()))
        if arrFound2:
            arrFound.append([])
            arrFound[intLength].append(arrEncoding[i])
            arrFound[intLength].append(arrFound2)
            if intChoice=="1":
                arrFound[intLength].append(str(binascii.hexlify(newChar.encode(arrEncoding[i]))))
            else:
                arrFound[intLength].append(str(binascii.hexlify(strChar.encode(arrEncoding[i]))))
            intLength = intLength + 1
        else:
            toRemove.append(i)         
    except:
        print("Possible Error - Encoding: "+ str(arrEncoding[i]))
        toRemove.append(i)


#Records uit array halen: Coderingsmethoden die niet functioneren op het woord        
for i in range(0,len(toRemove)):
    del(arrEncoding[toRemove[i]])
    for j in range(0,len(toRemove)):
        toRemove[j] = toRemove[j] - 1
   
#Resultaten printen        
print("\n RESULTS \n")
print("Encoding:\tHexed value:\tOffset:")
for i in range(0,len(arrFound)):
        print(str(arrEncoding[i]) + ":\t" + arrFound[i][2][2:len(arrFound[i][2])-1] + "\t" + str(arrFound[i][1]))
        print("Found: " + str(len(arrFound[i][1])))

#Aantal unieke entries bepalen en weergeven (offsets)
setExist = set()
arrDedup = []
for i in range(0,len(arrFound)):
    for item in arrFound[i][1]:
        if item not in setExist:
            arrDedup.append(item)
            setExist.add(item)
      
count = 0
if len(arrDedup) == 0:
    for i in range(0,len(arrFound[i])):
        if arrFound[i][1]:
            count = count + len(arrFound[i][1])
    print("\nUnique amount of offsets of all encoding methods: " + str(count))
else:
    print("\nUnique amount of offsets of all encoding methods: " + str(len(arrDedup)))
