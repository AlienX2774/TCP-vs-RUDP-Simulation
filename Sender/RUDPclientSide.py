import hashlib
import socket
from datetime import datetime, time
import os
eof = "-1".encode('utf8')
serverAddress = '000.000.0.0'  # enter ip address here
serverPort = 59921
fileName = "send.txt"
totalTime = 0
it = []
numTimesSend = 50
seqNum = 30000
bytesData = seqNum.to_bytes(5, "little")
print('Connecting to server side: ', serverAddress, '\n')
bufferSize = 8192
for x in range(numTimesSend):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (serverAddress, serverPort)
    fileName = "send.txt"
    statinfo = os.stat(fileName)
    print('Sending the file for the ', x + 1, 'th  time.')
    file_to_send = open(fileName, 'rb')
    fileData = file_to_send.read(bufferSize - 5)
    data = bytesData + fileData
    packetsToSend = statinfo.st_size / bufferSize
    startTime = datetime.now()
    for j in range(int(packetsToSend) + 1):
        try:
            sock.settimeout(0.600)
            sent = sock.sendto(data, server_address)
        except socket.timeout:
            sent = sock.sendto(data, server_address)
        try:
            sock.settimeout(2)
            adk, server = sock.recvfrom(bufferSize)
        except socket.timeout:
            sent = sock.sendto(data, server_address)
            adk, server = sock.recvfrom(bufferSize)

        adk = int.from_bytes(adk, "little")
        if adk == seqNum + 1:
            seqNum += 1
            fileData = file_to_send.read(bufferSize - 5)
            bytesData = seqNum.to_bytes(5, "little")
            data = bytesData + fileData

        else:
            print("The Acknowledgment is: ", adk, " and Sequence Number is: ",
                  seqNum + 1, ". They did not match.")
            sock.settimeout(0.800)
            sent = sock.sendto(data, server_address)
            try:
                sock.settimeout(0.800)
                adk, server = sock.recvfrom(bufferSize)
                sent = sock.sendto(data, server_address)
                adk, server = sock.recvfrom(bufferSize)
                adk = int.from_bytes(adk, "little")
            except socket.timeout:
                sock.settimeout(0.800)
                sent = sock.sendto(data, server_address)
                adk, server = sock.recvfrom(bufferSize)
                adk = int.from_bytes(adk, "little")
            if adk == seqNum + 1:
                seqNum += 1
                fileData = file_to_send.read(bufferSize - 5)
                bytesData = seqNum.to_bytes(5, "little")
                data = bytesData + fileData

        if data[5:] == b'':
            test = False
            break
    try:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
    except socket.timeout:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
        print("Did not send eof.")

    try:
        sock.settimeout(0.600)
        adk, server = sock.recvfrom(bufferSize)
    except socket.timeout:
        sock.settimeout(0.600)
        sent = sock.sendto(eof, server_address)
        adk, server = sock.recvfrom(bufferSize)
    adk = adk[:5]
    adk = int.from_bytes(adk, "little")
    if adk == seqNum:
        print("Got adk from server for the ", x+1, "th time")
        print('Finishing sending file',
              fileName, ' for the ', x+1, 'th  time')
        file_to_send.close()
        endTime = datetime.now()
        timeTaken = int((endTime - startTime).total_seconds() * 1000)
        totalTime += timeTaken
        it.append(timeTaken)
        print('The time required to send the file for ',
              x+1, 'th time is: ', timeTaken, "ms.\n")
        sock.close()
print('The average time to send the file is: ', totalTime/numTimesSend)
print('Total time to send the file for ',
      numTimesSend, ' times is: ', totalTime)
print('Task Complete.')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (serverAddress, serverPort)
BLOCKSIZE = 65536
hasher = hashlib.sha1()
with open(fileName, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
sock.settimeout(10)
sent = sock.sendto(hasher.hexdigest().encode('utf8'), server)
sock.close
name = "RUDPclientplotdata.txt"
with open(name, 'w') as file:
    for d in it:
        file.write('%d\n' % d)
