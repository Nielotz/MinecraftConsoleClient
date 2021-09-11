import logging

loggers = dict()


def get_logger(name: str):
    if name not in loggers:
        loggers[name] = logging.getLogger(name)

        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        loggers[name].addHandler(ch)

    return loggers[name]
