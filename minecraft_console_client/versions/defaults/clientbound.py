class Clientbound:
    """
    Namespace for clientbound events (sent by server).
    Method names same as on minecraft protocol page.

    Inherits default methods from versions.default.Server.

    :params bot: Bot on which process packet.
    :params bytes: Data received from server, uncompressed, without packet id.

    Sample methods:
    
        @staticmethod
    def entity_teleport(bot, data: bytes):
        pass

    @staticmethod
    def advancements(bot, data: bytes):
        pass
    """
    pass
