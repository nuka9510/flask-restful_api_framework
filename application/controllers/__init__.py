from system.core.framework import app
from . import Example

app.register_blueprint(Example.bp)