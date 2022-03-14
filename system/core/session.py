import os, re, ast, string, random
from application import config
from system import Input

class Session(Input):
    def __init__(self):
        '''
        method

        session_id()

        set(key: str, value: str|int|...)

        get(key: str)

        pop(key: str)

        clear()
        '''
        super().__init__()
        self.__is_clear = False
        self.__session_id = None
        self.__session_path = None

    def __set_session_id(self):
        self.__session_id = ''
        string_pool = string.ascii_letters + string.digits

        for i in range(50):
            self.__session_id += random.choice(string_pool)

        if os.path.exists(os.path.join(config['SESSION_PATH'], f"{config['SESSION_NAME']}{self.__session_id}")):
            self.__set_session_id()
        else:
            self.__set_session_path()

    def __get_session_id(self):
        if not self.__session_id:
            if config['SESSION_STORAGE'] == 'headers':
                session_id = self.arg('Authorization', location=config['SESSION_STORAGE'])

                if session_id:
                    self.__session_id = re.sub('^Bearer ', '', session_id)
            else:
                session_id = self.arg(config['SESSION_NAME'], location=config['SESSION_STORAGE'])

                if session_id:
                    self.__session_id = session_id

    def __set_session_path(self):
        if not self.__session_id:
            self.__get_session_id()
            self.__set_session_path()
        else:
            if not self.__session_path:
                self.__session_path = os.path.join(config['SESSION_PATH'], f"{config['SESSION_NAME']}{self.__session_id}")

    def __close(self):
        self.__is_clear = False
        self.__session_id = None
        self.__session_path = None

    def _set_header(self):
        session_id = self.__session_id

        self.__close()

        if config['SESSION_STORAGE'] == 'headers':
            return (config['SESSION_NAME'], session_id)
        elif config['SESSION_STORAGE'] == 'cookies':
            return ('Set-Cookie', f"{config['SESSION_NAME']}="+(session_id if not session_id is None else '; Expires=0'))

    def set(self, key, value):
        '''
        set(key: str, value: str|int|...)

        session에 key, value를 담는다.
        '''
        self.__get_session_id()

        r = None

        if not self.__session_id:
            self.__set_session_id()
        else:
            self.__set_session_path()

        if not os.path.exists(config['SESSION_PATH']):
            os.makedirs(config['SESSION_PATH'])
        
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
        '''
        get(key: str)

        session에서 해당 key의 value를 가져온다.
        '''
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
        '''
        pop(key: str)

        session에서 해당 key를 지운다.
        '''
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
        '''
        clear()

        session을 지운다.
        '''
        self.__get_session_id()
        self.__set_session_path()
        os.remove(self.__session_path)

        self.__is_clear = True
        self.__session_id = None
        self.__session_path = None
    
    def session_id(self):
        '''
        session_id()

        session의 id를 가져온다.
        '''
        result = None

        if not self.__is_clear:
            self.__get_session_id()

            result = self.__session_id

        return result