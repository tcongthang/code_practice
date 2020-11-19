import time
import logging


class Helper(object):

    def __init__(self):
        self.nTime = 5

    def sleep(self, nTime=None):
        if nTime is None:
            nTime = self.nTime
        self.fwrite('Sleeping for .... %s seconds ....' % nTime)
        time.sleep(nTime)

    def fwrite(self, msg):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', filemode='w')
        # Creating an object
        logger = logging.getLogger()
        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.INFO)
        fwrite = logging.info
        return fwrite(msg)
