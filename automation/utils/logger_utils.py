import logging

logging.basicConfig(filename="logger.log", 
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG,
                    filemode='w')
logger : logging.Logger = logging.getLogger(__name__)