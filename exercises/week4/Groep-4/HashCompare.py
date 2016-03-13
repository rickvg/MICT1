import threading
import time
import hashlib

#print(arrClusters)
def CheckHash(line):
    try:
        arrHashes = []
        if int(line.split(",")[4]) < 4096 and int(line.split(",")[4]) > 2: #Size of file must be smaller than 4096 in order to be in RAM/Drive Slack. Size larger than two to prevent false positives.
            with open("DATAFILTERED", "rb") as newfile:
                number = 1
                number2 = 0
                while number < 4:
                    count = int(line.split(",")[4])
                    while count+(number2*4096) < number*4096:
                        newfile.seek(count+(number2*4096))
                        toHash = newfile.read(int(line.split(",")[4]))
                        arrHashes.append(hashlib.md5(toHash).hexdigest().upper())
                        count = count + 1
                    number2 = number2 + 1
                    number = number + 1
            for i in range(0,len(arrHashes)):
                if arrHashes[i] in line.split(",")[1]:
                    print(line.split(",")[1])
                    print(arrHashes[i])
                    print(newfile.tell()) #Print File position end
                    print(newfile.tell()-int(line.split(",")[4])) #Print File position start
    except:
        print("Error in thread")
    #Done with thread

threads = []

with open("NSRLFile.txt", "r", encoding="latin1") as f:
    for line in f:
        blnActive = False
        while blnActive == False:
            if threading.active_count() > 200:
                blnActive = False
                time.sleep(3)
            else:
                blnActive = True
                t = threading.Thread(target=CheckHash, args=(line,))
                threads.append(t)
                t.start()

#Wait for all threads to finish
for x in threads:
    x.join()
