import logging
import errno
import os
import shutil

LOG_PATH = '/tmp/marketsim/'

""" resetLogs deletes the logs folder """


def resetLogs():
    # TODO: remove this and put proper error checking for next line
    mkdir_p(LOG_PATH)
    shutil.rmtree(LOG_PATH)


def mkdir_p(path):
    """http://stackoverflow.com/a/600612/190597 (tzot)"""
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

""" newLogger creates and returns a logger for an object. For example, newLogger("agent", "123") should be called for an agent with ID 123. The log will be found in /tmp/marketsim/agent/123.log """


def newLogger(logType, logID):
    logPath = LOG_PATH + str(logType)
    mkdir_p(logPath)
    logFilename = logPath + "/" + str(logID) + ".log"
    logger = logging.getLogger(str(logID))
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    f = logging.FileHandler(logFilename, mode="w",)
    logger.addHandler(f)
    return logger
