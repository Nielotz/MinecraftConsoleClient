import logging

# TODO: improve logger.
logger = logging.getLogger("mainLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# fh = logging.FileHandler()
# fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

import run

if __name__ == "__main__":
    run.run()
