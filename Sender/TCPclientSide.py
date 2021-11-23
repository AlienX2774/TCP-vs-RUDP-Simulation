import socket
from datetime import datetime
import hashlib
host = '000.000.0.0'  # enter ip address here
port = 59921
fileName = "send.txt"
totalTime = 0
it = []
numTimesSend = 50
bufferSize = 8192
print('Connecting to server side: ', host, '\n')
for x in range(numTimesSend):
    s = socket.socket()
    s.connect((host, port))
    print('Sending file for the ', x+1, 'th  time.')
    file_to_send = open(fileName, 'rb')
    startTime = datetime.now()
    data = file_to_send.read(bufferSize)
    while data:
        s.send(data)
        data = file_to_send.read(bufferSize)
    print('Finished sending file for the ', x, 'th  time')
    file_to_send.close()
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    it.append(timeTaken)
    print('The time required to send the file for the ',
          x, 'th time is: ', timeTaken, "ms.\n")
    s.close()
print('The average time taken to send the file is: ',
      totalTime/numTimesSend, 'ms.\n')
print('Total time to send the file ', numTimesSend,
      ' times is: ', totalTime, 'ms\n')
print('Task Completed.')
s = socket.socket()
s.connect((host, port))
BLOCKSIZE = 65536
hasher = hashlib.sha1()
with open(fileName, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
s.send(hasher.hexdigest().encode('utf8'))
s.close()
name = "TCPclientplotdata.txt"
with open(name, 'w') as file:
    for d in it:
        file.write('%d\n' % d)
