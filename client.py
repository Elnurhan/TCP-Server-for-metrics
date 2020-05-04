import socket
import time


class ClientError(Exception):
    '''Выбрасывается в случае неуспешной отправки'''
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        try:
            self.connection = socket.create_connection((self.ip, self.port), timeout)
        except socket.error as err:
            print(err)

    def _response_parser(self, resp):
        #message = self.connection.recv(1024).decode()
        message = resp.decode()
        response = message.split()
        if response[0] == 'error':
            raise ClientError
        elif len(response) == 4:
            print({})


    def put(self, name, value, timestamp=int(time.time())):
        request = f'put {name} {value} {timestamp}\n'
        try:
            self.connection.sendall(request.encode("utf-8"))
        except socket.error as err:
            raise ClientError("Client error: Put")

        self._response_parser(self.connection.recv(1024))

    def get(self, name):
        request = f'get {name}\n'
        try:
            self.connection.sendall(request.encode("utf-8"))
        except socket.error as err:
            raise ClientError("Client Error: Get")
        
        self._response_parser(self.connection.recv(1024))
        #return self.connection.recv(1024).decode()


    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            print(err)
