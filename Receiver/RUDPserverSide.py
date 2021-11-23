import socket
from datetime import datetime
import hashlib
serverAddress = '000.000.0.0'  # enter ip address here
serverPort = 59921
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(15)
server_address = (serverAddress, serverPort)
s.bind(server_address)
totalTime = 0
it = []
print('Waiting for client to send request\n')
totalFilesCount = 50
i = 0
fileName = 'receive.txt'
bufferSize = 8192
startSeqNum = 30000
while True:
    i = i+1
    file = 'RUDPRecevied/receive'+str(i)+'.txt'
    f = open(file, 'wb')
    startTime = datetime.now()
    data, server = s.recvfrom(bufferSize)
    print('Receiving the file for the ', i, 'th time.')
    check = True
    while data:
        fileSeqNum = data[:5]
        seqNum = int.from_bytes(fileSeqNum, "little")
        if startSeqNum == seqNum:
            seqNum += 1
            startSeqNum += 1
            adk = seqNum.to_bytes(5, "little")
            data = data[5:]
            f.write(data)
        else:
            adk = startSeqNum.to_bytes(5, "little")
        try:
            s.settimeout(0.600)
            sent = s.sendto(adk, server)
        except socket.timeout:
            s.settimeout(1)
            sent = s.sendto(adk, server)

        try:
            s.settimeout(2)
            data, server = s.recvfrom(bufferSize)
        except socket.timeout:
            sent = s.sendto(adk, server)
            data, server = s.recvfrom(bufferSize)

        eofData = data[5:]
        try:
            if data.decode('utf8') == '-1':
                fileSeqNum = data[:5]
                adk = seqNum.to_bytes(5, "little")
                sent = s.sendto(adk, server)
                f.close
                break
        except UnicodeDecodeError:
            error = "decode error"
    endTime = datetime.now()
    if i == 1:
        timeTaken = int((endTime - startTime).total_seconds())
    else:
        timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    it.append(timeTaken)
    print('Finished receiving file for the ', i, 'th time.')
    print('Time required to receive the file for the ',
          i, 'th time is: ', timeTaken, 'ms\n')
    if i == totalFilesCount:
        break
    try:
        seqNum += 1
        adk = seqNum.to_bytes(5, "little")
        s.settimeout(0.600)
        sent = s.sendto(adk, server)
    except socket.timeout:
        s.settimeout(1)
        sent = s.sendto(adk, server)
print('The average time to receive the file is: ',
      totalTime/totalFilesCount, 'ms.\n')
print('Total time to receive the file for ',
      totalFilesCount, ' times is: ', totalTime, 'ms.\n')
f = 0
hashFun, server = s.recvfrom(bufferSize)
s.close()
for x in range(totalFilesCount):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    x += 1
    with open('RUDPRecevied/receive'+str(x)+'.txt', 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
        if hashFun.decode('utf8') != hasher.hexdigest():
            f += 1
print(f, '/', totalFilesCount, 'files are corrupted.')
print('Task Completed')
name = "RUDPserverplotdata.txt"
with open(name, 'w') as file:
    for d in it:
        file.write('%s\n' % d)
