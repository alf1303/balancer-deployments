import logging

def get_logger(mod_name: str) -> logging.Logger:
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = get_logger(__name__)

def loginfo(msg):
    logger.info(msg)

def loglog(msg):
    logger.info(msg)