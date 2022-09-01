#logging
import logging

logging.basicConfig(filename="price.log", level=logging.DEBUG, format="%(asctime)s: %(message)s", datefmt='%H:%M:%S')

def debug_logger(string):
    logging.info(string)