import logging
import logging.config
import os

logPath = '.\\log'
if not os.path.exists(logPath):
    os.mkdir(logPath)

#config = {    "key1":"value1"     }
logging.config.fileConfig("./src/config/logger.conf")
logger = logging.getLogger("bz")