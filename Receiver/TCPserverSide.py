import socket
from datetime import datetime
import hashlib
HOST = '000.000.0.0'  # enter ip address here
PORT = 59921
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
totalTime = 0
it = []
print('Waiting for client to send request\n')
totalFilesCount = 50
bufferSize = 8192
i = 0
fileName = 'rec.txt'
while True:
    conn, addr = s.accept()
    startTime = datetime.now()
    i = i+1
    file = 'TCPRecevied/receive'+str(i)+'.txt'
    print('Receiving the file for the ', i, 'th time.')
    f = open(file, 'wb')
    data = conn.recv(bufferSize)
    while (data):
        f.write(data)
        data = conn.recv(bufferSize)
    f.close()
    print('Finished receiving file for the ', i, 'th time.')
    endTime = datetime.now()
    timeTaken = int((endTime - startTime).total_seconds() * 1000)
    totalTime += timeTaken
    it.append(timeTaken)
    print('Time required to receive the file for the ',
          i, 'th time is: ', timeTaken, 'ms\n')
    if i == totalFilesCount:
        break
    conn.close()
print('The average time to receive the file is: ',
      totalTime/totalFilesCount, 'ms.\n')
print('Total time to receive the file for ',
      totalFilesCount, ' times is: ', totalTime, 'ms.\n')
f = 0
conn, addr = s.accept()
hashFun = conn.recv(bufferSize)
for x in range(totalFilesCount):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    x += 1
    with open('TCPRecevied/receive'+str(x)+'.txt', 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    if hashFun.decode('utf8') != hasher.hexdigest():
        f += 1
print(f, '/', totalFilesCount, 'files are corrupted.')
print('Task Completed')
conn.close()
s.close()
name = "TCPserverplotdata.txt"
with open(name, 'w') as file:
    for d in it:
        file.write('%d\n' % d)
