import datetime
import logging
import os

from ELEC9609.Tools.Logger import Logger

try:
    logDirectory = 'logs'
    print('| INFO | Logger starting ...')
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)
    logging.basicConfig(level=logging.DEBUG, filename=logDirectory + '/log' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.log')
except Exception as e:
    Logger.error(e)
