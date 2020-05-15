import logging
logger = logging.getLogger("mainLogger")

from typing import NoReturn

from misc import utils
from misc.exceptions import DisconnectedError
from gui.gui import gui


def set_compression(bot, data: bytes):
    threshold = utils.unpack_varint(data)[0]
    bot._conn.set_compression(threshold)

    gui.set_value("compression threshold", threshold)

    if threshold < 0:
        logger.info(f"Compression is disabled")
    else:
        logger.info(f"Compression set to {threshold} bytes")


def login_success(bot, data: bytes) -> True:
    bot._player.uuid = utils.extract_string(data)[0].decode('utf-8')
    logger.info(f"Successfully logged to the server, "
                f"UUID: {bot._player.uuid}")
    return True


def disconnect(bot, data: bytes) -> NoReturn:
    reason = utils.extract_json_from_chat(data)[0]
    # reason should be dict Chat type.
    logger.error(f"{bot._player.username} has been "
                 f"disconnected by server. Reason: '{reason['text']}'")
    raise DisconnectedError("Disconnected by server.")