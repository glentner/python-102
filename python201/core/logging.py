import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from socket import gethostname


HOST = gethostname()
handler = logging.StreamHandler()
formatter = logging.Formatter(f'%(asctime)s {HOST} %(levelname)s [%(name)s] %(message)s')
handler.setFormatter(formatter)


def getLogger(name: str, level: str = 'warning') -> logging.Logger:
    """
    Create a named logger.

    Parameters:
        name (str): name for the logger
        level (str): logging level (default='warning')

    Returns:
        logger (`logging.getLogger`): the created logger instance

    See Also:
        `logging.getLogger`
    """
    log = logging.getLogger(name)
    log.addHandler(handler)
    log.setLevel(getattr(logging, level.upper()))
    return log