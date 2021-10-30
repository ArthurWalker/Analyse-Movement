import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formater = logging.Formatter('%(asctime)s:%(filename)s:%(levelname)s:%(lineno)d:%(message)s')

file_handler = logging.FileHandler('test.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formater)

stream_hanlder = logging.StreamHandler()
stream_hanlder.setLevel(logging.INFO)
stream_hanlder.setFormatter(formater)

logger.addHandler(file_handler)
logger.addHandler(stream_hanlder)
logger.setLevel(logging.INFO)