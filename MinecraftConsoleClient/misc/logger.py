import logging

loggers = dict()


def get_logger(name: str):
    if name not in loggers:
        loggers[name] = logging.getLogger(name)
        loggers[name].setLevel(level=logging.INFO)

    return loggers[name]

