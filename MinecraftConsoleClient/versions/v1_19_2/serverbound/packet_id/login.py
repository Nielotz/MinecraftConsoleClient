"""Contain packet name translated to its id."""

HANDSHAKE = LOGIN_START = b'\x00'
ENCRYPTION_RESPONSE = b'\x01'
LOGIN_PLUGIN_RESPONSE = b'\x02'
LEGACY_SERVER_LIST_PING = b'\xFE'
