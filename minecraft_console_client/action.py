import logging
logger = logging.getLogger('mainLogger')

from exceptions import DisconnectedError
from version import VersionNamedTuple, Version
from enum import Enum
import utils

""" Actions possible to happen, e.g. packets available to be received/sent. """


class Sever:
    """ Namespace for server-side events """

    @staticmethod
    def not_implemented():
        logger.debug("[2/2] Not implemented yet")

    @staticmethod
    def disconnect(player, data: bytes):
        reason = utils.extract_string_from_data(data)
        # reason should be dict Chat type.
        logger.error(f"[2/2] {player._data['username']} has been "
                     f"disconnected by server. Reason: {reason}")
        raise DisconnectedError("Disconnected by server.")

    @staticmethod
    def login_success(player, data: bytes):
        uuid, data = utils.extract_string_from_data(data)
        uuid = uuid.decode('utf-8')
        player._data["uuid"] = uuid

        logger.debug("[2/2] Successfully logged to the server")

    @staticmethod
    def set_compression(player, data: bytes):
        threshold, _ = utils.unpack_varint(data)
        player._conn.set_compression(threshold)

        if threshold < 0:
            logger.debug(f"[2/2] Compression is disabled")
        else:
            logger.debug(f"[2/2] Compression set to {threshold} bytes")


class Client:
    """ Namespace for client-side events """

    @staticmethod
    def not_implemented():
        logger.debug("[2/2] Not implemented yet")


def get_action_list(player_version: VersionNamedTuple) -> dict:
    """
    Returns dictionary that pairs packet_id to the action based on game version.

    :param player_version: VersionNamedTuple from Version
    :returns dict(int, method)
    :rtype dict
    """

    actions: dict = {
        "1.12.2": {
                0: Sever.disconnect,
                # 1: Sever._encryption_request,
                2: Sever.login_success,
                3: Sever.set_compression,
        }
    }
    try:
        actions_list = actions[player_version.release_name]
    except Exception:
        actions_list = None

    return actions_list
