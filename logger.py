import logging


def get_logger(name, level='INFO'):
    filename = '/Users/grofers/Downloads/prinder.log'

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    ch = logging.FileHandler(filename)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] -%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
