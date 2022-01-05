import socket
BUFFER_SIZE = 2

# client set ip and port to connect with sys.argv
s = socket.socket(2, 1)
s.connect(('192.168.1.110', 8000))


s.send(b'04amit0')
#s.send(b'04amit303guy')
#s.send(b'04amit303guy')
s.send(b'04amit503guy00000003hey')
while True:
    data = s.recv(1024)
    print(data)