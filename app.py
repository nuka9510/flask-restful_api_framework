import os
from flask import Flask
from application import config
from application.controllers import Example

app = Flask(__name__)

for key in config['APP']:
    app.config[key] = config['APP'][key]

app.register_blueprint(Example.bp)

if not app.debug:
    from logging import FileHandler

    if not os.path.exists(config['LOG_PATH']):
        os.makedirs(config['LOG_PATH'])

    file_handler = FileHandler(filename=os.path.join(config['LOG_PATH'], config['LOG_NAME']))
    file_handler.setFormatter(config['LOG_FORMAT'])

    app.logger.setLevel(config['LOG_LEVEL'])
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()