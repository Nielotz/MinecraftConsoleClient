"""Module with functions related to given packet."""

import logging
from typing import NoReturn
from typing import TYPE_CHECKING

from data_structures.packet_data_reader import PacketDataReader
from misc import converters
from misc.exceptions import DisconnectedByServerException
from versions.v1_12_2.view.view import gui

if TYPE_CHECKING:
    import game

logger = logging.getLogger("mainLogger")


def set_compression(game_: "game.Game", packet_data_reader: PacketDataReader) -> None:
    threshold = converters.extract_varint_as_int(data)[0]

    gui.set_labels(("compression threshold", threshold))

    if threshold < 0:
        logger.info("Compression is disabled")
    else:
        logger.info("Compression set to %i bytes", threshold)

    return threshold


def login_success(game_: "game.Game", packet_data_reader: PacketDataReader) -> True:
    game_.data.hero.data.uuid = converters.extract_string_bytes(data)[0].decode('utf-8')
    logger.info("Successfully logged to the server, "
                "UUID: %s", game_.data.hero.data.uuid)
    return True


def disconnect(game_: "game.Game", packet_data_reader: PacketDataReader) -> NoReturn:
    # TODO: After implementing chat interpreter do sth here.
    reason = converters.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    try:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     game_.data.hero.data.username, reason['text'])
    except Exception:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     game_.data.hero.data.username, reason)
    raise DisconnectedByServerException("Disconnected by server.")
