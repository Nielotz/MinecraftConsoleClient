import socket

import logging
logging.basicConfig(level=logging.INFO)


class Server:
    ip = None
    domain_name = None
    port = None

    # TODO change params to class IP with ip parser, etc.
    def __init__(self, ip=None, domain_name=None,  port=None):
        if ip is not None:
            self.ip = ip
            logging.info(f"Server ip: '{ip}'")
        if domain_name is not None:
            self.domain_name = domain_name
            logging.info(f"Server domain name: '{domain_name}'")
        if port is not None:
            self.port = port
            logging.info(f"Server port: '{port}'")

    def handshake(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.create_connection((self.domain_name, self.port))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
        print('Received', repr(data))
