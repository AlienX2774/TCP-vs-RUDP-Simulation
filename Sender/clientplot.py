import matplotlib.pyplot as plt
TCPclient = []
RUDPclient = []
with open('TCPclientplotdata.txt') as f:
    for line in f:
        TCPclient.append([int(x) for x in line.split()])
with open('RUDPclientplotdata.txt') as f:
    for line in f:
        RUDPclient.append([int(x) for x in line.split()])
plt.plot(TCPclient, label='TCP')
plt.plot(RUDPclient, label='RUDP')
plt.legend(title="Legend")
plt.xlabel('Files')
plt.ylabel('Time(ms)')
plt.title("Sender Side")
plt.show()
