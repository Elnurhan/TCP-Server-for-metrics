import asyncio


class Data:
    '''Хранилище метрик'''
    def __init__(self):
        self.storage = {}

    def put(self, name, value, timestamp):
       # Добавления метрики в хранилище
        if name not in self.storage:
            self.storage[name] = {}
        self.storage[name][int(timestamp)] = float(value)

    def get(self, name):
        # Возвращение метрики с хранилища, в отсортированном виде
        data = self.storage
        if name not in self.storage and name != '*':
            return 'ok\n\n'
        elif name != '*':
            data = {name: data.get(name, {})}

        result = {}
        for k, v in data.items():
            result[k] = sorted(v.items())

        return result

storage = Data()

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        #resp = process_data(data.decode())
        #self.transport.write(respo.encode())
        print(data.decode())
        self.response(data.decode())

    def response(self, data):
        data = data.split()
        if data[0] == 'put' and len(data) == 4:
            self.put(data[1], data[2], data[3])
            self.transport.write('ok\n\n'.encode('utf-8'))
        elif data[0] == 'get' and len(data) == 2:
            response = self.get(data[1])
            self.transport.write(response)
        else:
            self.transport.write('error\nwrong command\n\n'.encode('utf-8'))

    def put(self, name, value, timestamp):
        storage.put(name, value, timestamp)

    def get(self, name):
        response = storage.get(name)
        response = self._response_creater(response)
        return response

    def _response_creater(self, response):
        result = 'ok\n'
        if len(response) == 4: # Если ответ пуст, то ничего не возвращаем
            result += '\n'
            return result.encode('utf-8')
        for k, v in response.items():
            for i, v1 in v:
                result += f'{k} {i} {v1}\n'
        result += '\n'
        return result.encode('utf-8')
        


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )   

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 8181)
