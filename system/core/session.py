import os, ast, string, random
from application import config
from system import Input

class Session(Input):
    def __init__(self):
        super().__init__()
        self.__session_id = None

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
            self.__session_id = self.arg('sb_session', location='headers')

            if not self.__session_id:
                self.__session_id = self.arg('sb_session', location='cookies')

    def __set_session_path(self):
        self.__session_path = os.path.join(config['SB_SESSION_PATH'], f'sb_session{self.__session_id}')

    def set(self, key, value):
        self.__get_session_id()

        r = None

        if not self.__session_id:
            self.__set_session_id()
        else:
            self.__set_session_path()

        if not os.path.exists(config['SB_SESSION_PATH']):
            os.makedirs(config['SB_SESSION_PATH'], mode = 0o777)
        
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
            os.remove(self.__session_path)
        else:
            f = open(self.__session_path, 'w')

            f.write(str(r))
            f.close()

    def clear(self):
        self.__get_session_id()
        self.__set_session_path()

        os.remove(self.__session_path)
    
    def session_id(self):
        result = self.__session_id
        self.close()
        return result

    def close(self):
        self.__session_id = None