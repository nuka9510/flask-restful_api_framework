from flask import Flask
from application import config

app = Flask(__name__)

app.config = config['app']