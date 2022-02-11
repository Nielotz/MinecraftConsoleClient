"""Module with functions related to given packet."""
from enum import Enum
from typing import NoReturn, TYPE_CHECKING, NamedTuple

from misc import converters
from misc.exceptions import DisconnectedByServerException
from misc.logger import get_logger
from versions.v1_12_2.view.view import gui

if TYPE_CHECKING:
    import game

logger = get_logger("mainLogger")


class PacketType(NamedTuple):
    SetCompression = 1

class Packet:
    def __init__(self, data: memoryview, packet_type: PacketType):
        self.data: memoryview = data
        self.packet_type: PacketType = packet_type

    def parse(self):


def set_compression(game_: "game.Game", data: memoryview) -> None:
    # TODO PARSER_ADD_THRESHOLD: add call game.set_threshold
    threshold = converters.extract_varint_as_int(data)[0]

    # TODO GUI_IA: More separate GUI.
    gui.set_labels(("compression threshold", threshold))

    if threshold < 0:
        logger.info("Compression is disabled")
    else:
        logger.info("Compression set to %i bytes", threshold)

    return threshold


def login_success(game_: "game.Game", data: memoryview) -> True:
    game_.data.hero.uuid = converters.extract_string_bytes(data)[0].decode('utf-8')
    logger.info("Successfully logged to the server, "
                "UUID: %s", game_.data.hero.uuid)
    return True


def disconnect(game_: "game.Game", data: memoryview) -> NoReturn:
    # TODO: After implementing chat interpreter do sth here.
    reason = converters.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    try:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     game_.data.hero.username, reason['text'])
    except Exception:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     game_.data.hero.username, reason)
    raise DisconnectedByServerException("Disconnected by server.")
