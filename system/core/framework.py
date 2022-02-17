from flask import Flask
from application import config

app = Flask(__name__)

for key in config['app']:
    app.config[key] = config['app'][key]