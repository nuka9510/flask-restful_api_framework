from system import app
from . import Example

app.register_blueprint(Example.bp)