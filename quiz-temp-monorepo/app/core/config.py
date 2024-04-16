import logging


def logger_config(module):
    """
    Logger function.
    - can Extend Python loggin module and set a custom config.
    """
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(module)

    return logger
