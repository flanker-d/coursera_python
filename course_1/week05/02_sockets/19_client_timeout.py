# client
import socket
create_timeout = 5
with socket.create_connection(("127.0.0.1", 10001), create_timeout) as sock:
    sock.settimeout(2)
    try:
        sock.sendall("ping".encode("utf8"))
    except socket.timeout:
        print("send data error")
    except socket.error as ex:
        print("send data error:", ex)