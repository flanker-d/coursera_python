import socket
import time

class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.sock.close()

    def put(self, metric, value, timestamp=None):
        if timestamp == None:
            timestamp = int(time.time())
        request = "put " + metric + " " + str(value) + " " + str(int(timestamp)) + "\n"
        try:
            self.sock.sendall(request.encode())
            data = self._read()
            if data != 'ok\n\n':
                raise ClientError('Server returns an error')
        except:
            raise ClientError

    def _parse_answer_item(self, result, items_data):
        items = items_data.split()
        if len(items) == 3:
            key = str(items[0])
            timestamp = int(items[2])
            metric = float(items[1])
            value = (timestamp, metric)
            if key not in result:
                result[key] = list()
            result[key].append(value)
        else:
            raise ClientError

        return result

    def _parse_answer(self, data):
        result = {}
        if data == "ok\n\n":
            return result
        raw_data = data[3:-2]
        answer_list = raw_data.split('\n')

        if len(answer_list) > 0:
            for item in answer_list:
                result = self._parse_answer_item(result, item)
        return result

    def _process_data(self, data):
        if not data:
            raise ClientError
        if data == "error\nwrong command\n\n":
            raise ClientError
        if not data.startswith("ok\n"):
            raise ClientError
        return self._parse_answer(data)

    def _read(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.sock.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)

        return data.decode()

    def get(self, metric):
        request = "get " + metric + "\n"
        try:
            self.sock.sendall(request.encode())
            data = self._read()
            return self._process_data(data)
        except:
            raise ClientError

if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, 15)
    client.put(metric='palm.cpu', value=0.5, timestamp=1150864247)
    client.put(metric='palm.cpu', value=0.7, timestamp=1150864257)
    client.put(metric='eardrum.cpu', value=0.5, timestamp=1150864247)
    print(client.get("*"))
    print(client.get("zzz"))

