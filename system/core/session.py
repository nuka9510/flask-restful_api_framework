import os, ast, string, random
from application import config
from system import Input

class Session(Input):
    def __init__(self):
        super().__init__()
        self.__is_clear = False
        self.__session_id = None
        self.__session_path = None

    def __set_session_id(self):
        self.__session_id = ''
        string_pool = string.ascii_letters + string.digits

        for i in range(50):
            self.__session_id += random.choice(string_pool)

        if os.path.exists(os.path.join(config['SB_SESSION_PATH'], f'sb_session{self.__session_id}')):
            self.__set_session_id()
        else:
            self.__set_session_path()

    def __get_session_id(self):
        if not self.__session_id:
            self.__session_id = self.arg('sb_session', location=config['SB_SESSION_STORAGE'])

    def __set_session_path(self):
        if not self.__session_id:
            self.__get_session_id()
            self.__set_session_path()
        else:
            if not self.__session_path:
                self.__session_path = os.path.join(config['SB_SESSION_PATH'], f'sb_session{self.__session_id}')

    def _set_header(self):
        session_id = self.__session_id

        self.close()

        if config['SB_SESSION_STORAGE'] == 'headers':
            return ('sb_session', session_id)
        elif config['SB_SESSION_STORAGE'] == 'cookies':
            return ('Set-Cookie', f'sb_session='+(session_id if not session_id is None else '; Expires=0'))

    def set(self, key, value):
        self.__get_session_id()

        r = None

        if not self.__session_id:
            self.__set_session_id()
        else:
            self.__set_session_path()

        if not os.path.exists(config['SB_SESSION_PATH']):
            os.makedirs(config['SB_SESSION_PATH'], mode=0o777)
        
        if not os.path.exists(self.__session_path):
            r = {
                key: value
            }
        else:
            f = open(self.__session_path, 'r')
            r = f.readline()
            r = ast.literal_eval(r)
            r[key] = value

            f.close()

        f = open(self.__session_path, 'w')

        f.write(str(r))
        f.close()

    def get(self, key):
        self.__get_session_id()
        self.__set_session_path()

        r = None

        if os.path.exists(self.__session_path):
            f = open(self.__session_path, 'r')

            try:
                r = ast.literal_eval(f.readline())[key]
            except KeyError:
                pass

            f.close()

        return r

    def pop(self, key):
        self.__get_session_id()
        self.__set_session_path()

        f = open(self.__session_path, 'r+')
        r = ast.literal_eval(f.readline())

        f.close()
        r.pop(key)

        if not r:
            self.clear()
        else:
            f = open(self.__session_path, 'w')

            f.write(str(r))
            f.close()

    def clear(self):
        self.__get_session_id()
        self.__set_session_path()
        os.remove(self.__session_path)

        self.__is_clear = True
        self.__session_id = None
        self.__session_path = None

    def close(self):
        self.__is_clear = False
        self.__session_id = None
        self.__session_path = None
    
    def session_id(self):
        result = None

        if not self.__is_clear:
            self.__get_session_id()

            result = self.__session_id

        return result