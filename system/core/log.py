import os, logging
from application import config

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename=os.path.join(config['LOG_PATH'], config['LOG_NAME']))

file_handler.setFormatter(config['LOG_FORMAT'])

logger.setLevel(config['LOG_LEVEL'])
logger.addHandler(file_handler)