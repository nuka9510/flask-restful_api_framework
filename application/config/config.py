import os, logging
from datetime import datetime, timedelta

config = {
    'APP':{
        'ENV': 'production',
        'DEBUG': True,
        'TESTING': False,
    },
    'ENCRYPTION_SALT': '[YOURT_SALT_KEY]',
    'UPLOAD_PATH': os.path.join('[UPLOAD_PATH]'),
    'XSS_FILTER': True,
    'SESSION_NAME': 'session',
    'SESSION_PATH': os.path.join('application', 'sessions'),
    'SESSION_EXPIRE': timedelta(days=30),
    'LOG_PATH': os.path.join('application', 'logs'),
    'LOG_NAME': datetime.now().strftime('log-%Y-%m-%d.log'),
    'LOG_LEVEL': logging.WARNING,
    'LOG_FORMAT': logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'),
    'DATABASE': {
        'host': "[HOST]",
        'port': "[PORT]",
        'user': "[USER]",
        'password': "[PASSWORD]",
        'database': "[DATABASE]",
        # 'autocommit': True,
        # 'buffered': True,
    }
}