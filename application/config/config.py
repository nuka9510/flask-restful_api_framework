from system.core.framework import app
from datetime import timedelta

app.config = {
    'ENV': 'production',
    'DEBUG': True,
    'TESTING': False,
    'PROPAGATE_EXCEPTIONS': None,
    'PRESERVE_CONTEXT_ON_EXCEPTION': None,
    'TRAP_HTTP_EXCEPTIONS': False,
    'TRAP_BAD_REQUEST_ERRORS': None,
    'SECRET_KEY': None, # $ python -c "import secrets; print(secrets.token_hex())"
    'SESSION_COOKIE_NAME': 'session',
    'SESSION_COOKIE_DOMAIN': None,
    'SESSION_COOKIE_PATH': '/application/sessions',
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': False,
    'SESSION_COOKIE_SAMESITE': None,
    'PERMANENT_SESSION_LIFETIME': timedelta(days=31),
    'USE_X_SENDFILE': False,
    'SEND_FILE_MAX_AGE_DEFAULT': None,
    'SERVER_NAME': '[SERVER_NAME]',
    'APPLICATION_ROOT': '/',
    'PREFERRED_URL_SCHEME': 'http',
    'MAX_CONTENT_LENGTH': None,
    'JSON_AS_ASCII': True,
    'JSON_SORT_KEYS': True,
    'JSONIFY_PRETTYPRINT_REGULAR': False,
    'JSONIFY_MIMETYPE': 'application/json',
    'TEMPLATES_AUTO_RELOAD': None,
    'EXPLAIN_TEMPLATE_LOADING': False,
    'MAX_COOKIE_SIZE': 4093
}