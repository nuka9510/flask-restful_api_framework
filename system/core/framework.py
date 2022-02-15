from flask import Flask
from application.config import config

app = Flask(__name__)

app.config = config.config