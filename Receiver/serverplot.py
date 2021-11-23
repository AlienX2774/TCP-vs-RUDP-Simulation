import matplotlib.pyplot as plt
TCPserver = []
RUDPserver = []
with open('TCPserverplotdata.txt') as f:
    for line in f:
        TCPserver.append([int(x) for x in line.split()])
with open('RUDPserverplotdata.txt') as f:
    for line in f:
        RUDPserver.append([int(x) for x in line.split()])
plt.plot(TCPserver, label='TCP')
plt.plot(RUDPserver, label='RUDP')
plt.legend(title="Legend")
plt.xlabel('Files')
plt.ylabel('Time(ms)')
plt.title("Receiver Side")
plt.show()
