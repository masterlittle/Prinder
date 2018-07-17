import logging


def get_logger(name, level='INFO'):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    ch = logging.FileHandler('prinder.log')
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
