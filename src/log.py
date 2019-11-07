import logging
from logging.handlers import RotatingFileHandler


def Logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s')
    log_handler = RotatingFileHandler(
        'output/log/mail/mail.log', 'a', 5000000, 1)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
