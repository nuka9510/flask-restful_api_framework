from flask import Flask
from system.core.converter import *
from system.core.database import db
from application.config import app as app_config
from application.controllers import Example

app = Flask(__name__)

app.url_map.converters['regex'] = RegexConverter

for key in app_config:
    app.config[key] = app_config[key]

db.init_app(app)

app.register_blueprint(Example.bp)