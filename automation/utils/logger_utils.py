import logging

logging.basicConfig(filename="error_handling.log", 
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG,
                    filemode='w')
logger : logging.Logger = logging.getLogger(__name__)