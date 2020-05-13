class Creator:
    """
    Namespace for serverbound packets (created and sent by client).
    Method names same as on minecraft protocol page.

    """

    class Login:
        """ Namespace for packets used to login """
        pass

    class Status:
        """ Namespace for packets used to receive status """
        pass

    class Play:
        """ Namespace for packets used in play """
        pass
