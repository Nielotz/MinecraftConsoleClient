from typing import TYPE_CHECKING, Any

from misc import converters
from misc.exceptions import DisconnectedByServerException
from misc.logger import get_logger
from versions.v1_12_2.packet.clientbound.packet_specific import PacketSpecific
from versions.v1_12_2.view.view import gui

logger = get_logger("mainLogger")

if TYPE_CHECKING:
    import game


class SetCompression(PacketSpecific):
    threshold: int

    def read_data(self, data: memoryview):
        self.threshold = converters.extract_varint_as_int(data)[0]

    def default_handler(self, game_: "game.Game"):
        # TODO PARSER_ADD_THRESHOLD: add call game.set_threshold
        game_._connection.compression_threshold = self.threshold

        # TODO GUI_IA: More separate GUI.
        gui.set_labels(("compression threshold", self.threshold))

        if self.threshold < 0:
            logger.info("Compression is disabled")
        else:
            logger.info("Compression set to %i bytes", self.threshold)

        return self.threshold


class LoginSuccess(PacketSpecific):
    uuid: int

    def read_data(self, data: memoryview):
        self.uuid = converters.extract_string_bytes(data)[0].decode('utf-8')

    def default_handler(self, game_: "game.Game"):
        game_.data.hero.uuid = self.uuid
        logger.info("Successfully logged to the server, UUID: %s", game_.data.hero.uuid)
        return True


class Disconnect(PacketSpecific):
    reason: Any

    def read_data(self, data: memoryview):
        # TODO: After implementing chat interpreter do sth here.
        # reason should be dict Chat type.
        self.reason, _ = converters.extract_json_from_chat(data)

    def default_handler(self, game_: "game.Game"):
        try:
            logger.error("%s has been disconnected by server. Reason: '%s'",
                         game_.data.hero.username, self.reason['text'])
        except Exception:
            logger.error("%s has been disconnected by server. Reason: '%s'",
                         game_.data.hero.username, self.reason)
        raise DisconnectedByServerException("Disconnected by server.")
