# реализация сервера для тестирования метода get по заданию - Клиент для отправки метрик
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class Error(Exception):
    pass

sock = socket.socket()
sock.bind(('127.0.0.1', 8888))
sock.listen(1)

while True:
    conn, addr = sock.accept()

    print('Соединение установлено:', addr)

    # переменная response хранит строку возвращаемую сервером, если вам для
    # тестирования клиента необходим другой ответ, измените ее
    #response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'
    #response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\npalm.cpu not working\n\n'
    #response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\neardrum.cpu 1501864259 15\n\n'
    #response = b'ok\npalm.cpu 0.1 10\n\npalm.cpu 0.2 20\n\n'
    # response = b'ok\npalm.cpu 0.1 10\npalm.cpu 0.2 20\n\n'
    response = b'ok\n\n'
    #response = b'xyuta\n\n'
    #response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n\n\n'
    #response = b'error\nwrong command\n\n'

    while True:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            break
        if not data:
            break
        request = data.decode('utf-8')
        print('Получен запрос: {}'.format(ascii(request)))
        print('Отправлен ответ: {}'.format(ascii(response.decode("utf-8"))))
        conn.send(response)

    conn.close()