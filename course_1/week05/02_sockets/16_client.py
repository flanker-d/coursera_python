import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 10001))
sock.sendall("ping".encode())
sock.close()

#sock = socket.create_connection(("127.0.0.1", 10001))
#sock.sendall("ping".encode())
#sock.close()
