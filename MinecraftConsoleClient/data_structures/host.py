"""Holder for Host."""


class Host:
    """Hold and allow easy manipulation with host data."""

    socket_data: dict = {
        'host': None,
        'port': None
    }

    def __init__(self, host: str, port: int):
        """
        Create Host.

        Samples:
            Host("127.0.0.1", 25565)
            Host("localhost", 25565)

        :param host: hostname or ip address
        :param port: hostname or ip address
        """
        self.socket_data['host'] = host
        self.socket_data['port'] = port

    def get_host_data(self):
        """Return tuple(host, port)."""
        return self.socket_data['host'], self.socket_data['port']
