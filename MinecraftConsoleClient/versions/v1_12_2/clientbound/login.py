"""Module with functions related to given packet."""

import logging
from typing import NoReturn, TYPE_CHECKING

from misc import converters
from misc.exceptions import DisconnectedByServerException
from versions.v1_12_2.view.view import gui

if TYPE_CHECKING:
    import game

logger = logging.getLogger("mainLogger")


def set_compression(game_: "game.Game", data: memoryview) -> None:
    threshold = converters.extract_varint_as_int(data)[0]

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
