import logging


class Player:
    data = {
        "username": None,
        "version": 340  # 1.12.2 TODO: you know what
    }

    def __init__(self, username):
        self.data['username'] = username
        logging.info(f"Player data {self.data}")
