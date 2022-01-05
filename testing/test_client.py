import socket
BUFFER_SIZE = 2

# client set ip and port to connect with sys.argv
s = socket.socket(2, 1)
s.connect(('127.0.0.1', 8000))


s.send(b'03guy0')
s.send(b'03guy100000003hey')
#input('HANG')
#s.send(b'03guy100000003hey')
#s.send(b'03guy100000003hey')
#s.send(b'03guy100000003hey')

while True:
    data = s.recv(1024)
    print(data)



