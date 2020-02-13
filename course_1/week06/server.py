import asyncio

class DataBase:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self._db = {}

    def get(self, key):
        if key == "*":
            return self._db
        elif key in self._db:
            return {key: self._db[key]}
        else:
            return {}

    def put(self, key, value, timestamp):
        if key not in self._db:
            self._db[key] = {}
        self._db[key][timestamp] = value

class Parser:
    commands = ["put", "get"]

    @staticmethod
    def parse(data):
        cmd, params_body = data.split(" ", 1)
        params_body = params_body.strip()
        params = params_body.split(" ")

        ret = False
        if cmd == "get":
            if len(params) == 1:
                ret = True
        elif cmd == "put":
            if len(params) == 3:
                ret = True

        if ret == True:
            return (cmd, params)
        else:
            return ("err", [])


class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        #self.super().__init__()
        self._buffer = b""

    def connection_made(self, transport):
        self.transport = transport
        self._db = DataBase()

    def data_received(self, data):
        self._buffer += data
        try:
            decoded_data = self._buffer.decode()
        except UnicodeDecodeError:
            return

        # ждем данных, если команда не завершена символом \n
        if not decoded_data.endswith('\n'):
            return

        self._buffer = b''

        try:
            # обрабатываем поступивший запрос
            resp = self.process_data(decoded_data)
        except Exception as err:
            # формируем ошибку, в случае ожидаемых исключений
            self.transport.write("error\n{}\n\n".format(err).encode())
            return

        # формируем успешный ответ
        self.transport.write(resp.encode())

    def _process_get(self, params):
        key = params[0]
        dict = self._db.get(key)

        result = ""
        for key, val_list in dict.items():
            for ts, val in val_list.items():
                result += "{} {} {}\n".format(key, val, ts)

        return "ok\n{}\n".format(result)

    def _process_put(self, params):
        try:
            key = str(params[0])
            val = float(params[1])
            ts  = int(params[2])
            self._db.put(key, val, ts)
        except:
            return self._error()
        return "ok\n\n"

    def _error(self):
        return "error\nwrong command\n\n"

    def process_data(self, data):
        cmd, params = Parser.parse(data)
        #print (cmd, params)
        if cmd == "get":
            return self._process_get(params)
        elif cmd == "put":
            return self._process_put(params)
        else:
            return self._error()

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server("127.0.0.1", 8888)