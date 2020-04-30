import logging
logging.basicConfig(level=logging.INFO)


class Player:
    data = {
        "username": None,
        "password": None,
        "version": 340  # 1.12.2 TODO: you know what
    }

    def __init__(self, username, password=None):
        self.data['username'] = username
        self.data['password'] = password
        logging.info(f"Player data {self.data}")
