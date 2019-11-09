import logging
from logging.handlers import RotatingFileHandler
import os
from os import path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = "/output/log/"

'''
This function is to check if the file already exist in the directory config. If exist, we
do nothing else we create the file.
logName = the name of the log that need to be check
'''


def checkLogFileExist(logName):
    if not path.exists(BASE_DIR+LOG_DIR+logName+".txt"):
        logFile = open(BASE_DIR+LOG_DIR+logName+'.txt', 'x')
        logFile.close()


''' 
This function is used for write log.
logName = describe the name of the log to write and what the log is for.
level = level of log to be used. 4 levels used: INFO, DEBUG, WARNING, CRITICAL
message = the messsage who come with the level. Not limited in caractere. 
It describe the action done before logging.
'''


def writeLogFile(logName, level, message):
    # We check if file already exist or ifd we need to create it
    checkLogFileExist(logName)

    # Creation of the 'logger' which permit to write down the log
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(message)s')
    log_handler = RotatingFileHandler(
        BASE_DIR+LOG_DIR+logName+".txt", 'a', 5000000, 1)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    # here we write the log depending on it's level
    try:
        if level is 'info':
            logger.info(message)
    except level is 'debug':
        logger.debug(message)
    except level is 'warning':
        logger.warning(message)
    except level is 'critical':
        logger.critical(message)
