from typing import  TYPE_CHECKING

if TYPE_CHECKING:
    import game


class PacketSpecific:
    def read_data(self, data: memoryview):
        pass
    def pre_handler(self, game_: "game.Game"):
        pass
    def default_handler(self, game_: "game.Game"):
        pass
    def post_handler(self, game_: "game.Game"):
        pass
