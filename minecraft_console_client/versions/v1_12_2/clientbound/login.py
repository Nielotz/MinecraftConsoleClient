"""Module with functions related to given packet."""

import logging
from typing import NoReturn

from misc import converters
from misc.exceptions import DisconnectedError
from versions.v1_12_2.view.view import gui

logger = logging.getLogger("mainLogger")


def set_compression(bot, data: bytes) -> None:
    threshold = converters.extract_varint(data)[0]
    bot._conn.set_compression(threshold)

    gui.set_labels(("compression threshold", threshold))

    if threshold < 0:
        logger.info("Compression is disabled")
    else:
        logger.info("Compression set to %i bytes", threshold)


def login_success(bot, data: bytes) -> True:
    bot.game_data.player_data_holder.uuid = converters.extract_string(data)[0].decode(
        'utf-8')
    logger.info("Successfully logged to the server, "
                "UUID: %s", bot.game_data.player_data_holder.uuid)
    return True


def disconnect(bot, data: bytes) -> NoReturn:
    # TODO: After implementing chat interpreter do sth here.
    reason = converters.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    try:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     bot.game_data.player_data_holder.username, reason['text'])
    except Exception:
        logger.error("%s has been disconnected by server. Reason: '%s'",
                     bot.game_data.player_data_holder.username, reason)
    raise DisconnectedError("Disconnected by server.")
