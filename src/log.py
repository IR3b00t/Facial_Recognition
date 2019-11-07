import logging
from logging.handlers import RotatingFileHandler
import os
from os import path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = "/output/log/"


def checkLogFileExist(logName):
    if not path.exists(BASE_DIR+LOG_DIR+logName+".txt"):
        logFile = open(BASE_DIR+LOG_DIR+logName+'.txt', 'x')
        logFile.close()


def writeLogFile(logName, level, message):

    checkLogFileExist(logName)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s')
    log_handler = RotatingFileHandler(
        BASE_DIR+LOG_DIR+logName+".txt", 'a', 5000000, 1)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    try:
        if level is 'info':
            logger.info(message)
    except level is 'debug':
        logger.debug(message)
    except level is 'warning':
        logger.warning(message)
    except level is 'critical':
        logger.critical(message)
