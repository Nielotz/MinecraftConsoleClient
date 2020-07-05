class Host:
    socket_data: dict = {
        'host': None,
        'port': None
    }

    def __init__(self, host: str, port: int):
        self.socket_data['host'] = host
        self.socket_data['port'] = port

    def get_host_data(self):
        return self.socket_data['host'], self.socket_data['port']
