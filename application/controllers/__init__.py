from application.config.config import app
from . import Index

app.register_blueprint(Index.bp)