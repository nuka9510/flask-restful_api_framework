import os
from flask import Flask
from application import config

app = Flask(__name__)

for key in config['APP']:
    app.config[key] = config['APP'][key]

if not app.debug:
    from logging import FileHandler

    if not os.path.exists(config['LOG_PATH']):
        os.makedirs(config['LOG_PATH'])

    file_handler = FileHandler(filename=os.path.join(config['LOG_PATH'], config['LOG_NAME']))
    file_handler.setLevel(config['LOG_LEVEL'])
    file_handler.setFormatter(config['LOG_FORMAT'])
    app.logger.addHandler(file_handler)