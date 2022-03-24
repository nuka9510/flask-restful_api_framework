import os, re, ast, string, random, datetime
from flask import request
from application import config
from system import logger

class Session():
    def __init__(self):
        '''
        method

        session_id()

        session_exists()

        set(key: str, value: str|int|...)

        get(key: str)

        pop(key: str)

        clear()
        '''
        super().__init__()
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

    def __get_session_id(self, flag = True):
        if not self.__session_id:
            try:
                session_id = request.headers['Authorization']

                if session_id:
                    self.__session_id = re.sub('^Bearer ', '', session_id)
            except KeyError as e:
                if 'HTTP_AUTHORIZATION' in e.args:
                    logger.error("KeyError: request.headers['Authorization']")

        if flag:
            self.__set_session_path()

            if config['SESSION_EXPIRE']:
                if self.__session_id and self.__session_path:
                    self.__session_utime()
        else:
            self.__session_path = os.path.join(config['SESSION_PATH'], f"{config['SESSION_NAME']}{self.__session_id}")

            if not os.path.exists(self.__session_path):
                self.__close()
            else:
                if config['SESSION_EXPIRE']:
                    self.__session_utime()

    def __set_session_path(self):
        if not self.__session_id:
            self.__set_session_id()
        else:
            if not self.__session_path:
                self.__session_path = os.path.join(config['SESSION_PATH'], f"{config['SESSION_NAME']}{self.__session_id}")

                if not os.path.exists(config['SESSION_PATH']):
                    os.makedirs(config['SESSION_PATH'])

                if not os.path.exists(self.__session_path):
                    open(self.__session_path, 'w').close()

    def __session_utime(self):
        if datetime.datetime.now() <= (datetime.datetime.fromtimestamp(os.stat(self.__session_path).st_atime) + config['SESSION_EXPIRE']):
            os.utime(self.__session_path)
        else:
            self.clear()

    def __close(self):
        self.__session_id = None
        self.__session_path = None

    def set(self, key, value):
        '''
        set(key: str, value: str|int|...)

        session에 key, value를 담는다.
        '''
        self.__get_session_id()

        if self.__session_id and self.__session_path:
            f = open(self.__session_path, 'r')
            r = f.readline()

            if r:
                r = ast.literal_eval(r)
                r[key] = value
            else:
                r = dict(
                    key= value
                )

            f.close()

            f = open(self.__session_path, 'w')

            f.write(str(r))
            f.close()
            self.__close()
        else:
            self.set(key, value)

    def get(self, key):
        '''
        get(key: str)

        session에서 해당 key의 value를 가져온다.
        '''
        self.__get_session_id()
        r = None

        if self.__session_id and self.__session_path:
            if os.path.exists(self.__session_path):
                f = open(self.__session_path, 'r')

                try:
                    # r = ast.literal_eval(f.readline())[key]
                    r = f.readline()
                    
                    if r:
                        r = ast.literal_eval(r)[key]
                    else:
                        r = None
                except KeyError:
                    pass

                f.close()

            self.__close()

        return r

    def pop(self, key):
        '''
        pop(key: str)

        session에서 해당 key를 지운다.
        '''
        self.__get_session_id()

        if self.__session_id and self.__session_path:
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

            self.__close()

    def clear(self):
        '''
        clear()

        session을 지운다.
        '''
        self.__get_session_id()

        if self.__session_id and self.__session_path:
            os.remove(self.__session_path)
            self.__close()
    
    def session_id(self):
        '''
        session_id()

        session의 id를 가져온다.
        '''
        self.__get_session_id()
        
        if self.__session_id and self.__session_path:
            result = self.__session_id

            self.__close()

            return result
        else:
            self.session_id()

    def session_exists(self):
        self.__get_session_id(False)
        result = bool(self.__session_id)
        self.__close()

        return result