import os, ast, string, random, datetime, sys
from typing import Union, Optional
from flask import request
from application.config import config
from system import logger

class Session():
    def __init__(self):
        '''Session Class
        ```
        Example:
            from system import Session
            
            session = Session()
        ```'''
        self.__session_id = None
        self.__session_path = None

    def __set_session_id(self):
        '''session_id를 생성한다.'''
        self.__session_id = ''
        string_pool = string.ascii_letters + string.digits

        for i in range(50):
            self.__session_id += random.choice(string_pool)

        if os.path.exists(os.path.join(config['SESSION_PATH'], f"{config['SESSION_NAME']}{self.__session_id}")):
            self.__set_session_id()
        else:
            self.__set_session_path()

    def __get_session_id(self, flag: bool = True):
        '''header: Authorization에 담긴 session_id를 가져온다.
        ```
        Args:
            flag (bool, optional): __set_session_path() 실행 여부. Defaults to True.
        ```'''
        if not self.__session_id:
            try:
                self.__session_id = request.headers['Authorization']
            except KeyError as e:
                if 'HTTP_AUTHORIZATION' in e.args:
                    logger.error("KeyError: request.headers['Authorization']", exc_info = sys.exc_info())

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
        '''session데이터를 담을 파일을 생성한다.'''
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
        '''session의 expire를 갱신 해준다.'''
        if datetime.datetime.now() <= (datetime.datetime.fromtimestamp(os.stat(self.__session_path).st_atime) + config['SESSION_EXPIRE']):
            os.utime(self.__session_path)
        else:
            self.clear()

    def __close(self):
        '''session과의 연결을 끊는다.'''
        self.__session_id = None
        self.__session_path = None

    def set(self, key: str, value: Union[bool, str, int, float]):
        '''session에 key, value를 담는다.
        ```
        Args:
            key (str): session에 담을 데이터의 key
            value (Union[str, int, float]): session에 담을 데이터의 value
        ```'''
        self.__get_session_id()

        f = open(self.__session_path, 'r')
        r = f.readline()

        f.close()

        if r:
            r = ast.literal_eval(r)
            r[key] = value
        else:
            r = dict().fromkeys([key], value)

        f = open(self.__session_path, 'w')

        f.write(str(r))
        f.close()
        self.__close()

    def get(self, key: str) -> Optional[Union[bool, str, int, float]]:
        '''session에서 해당 key의 value를 가져온다.
        ```
        Args:
            key (str): session에서 가져올 데이터의 key

        Returns:
            Optional[Union[str, int, float]]: session에서 가져온 데이터의 value
        ```'''
        self.__get_session_id()

        r = None
        f = open(self.__session_path, 'r')

        try:
            r = f.readline()
            
            if r:
                r = ast.literal_eval(r)[key]
            else:
                r = None
        except KeyError:
            r = None

        f.close()
        self.__close()

        return r

    def pop(self, key: str):
        '''session에서 해당 key와 value를 지운다.
        ```
        Args:
            key (str): session에서 지울 데이터의 key
        ```'''
        self.__get_session_id()

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
        '''session을 지운다.'''
        self.__get_session_id()
        os.remove(self.__session_path)
        self.__close()
    
    def session_id(self) -> str:
        '''session의 id를 가져온다.
        ```
        Returns:
            str: session의 id
        ```'''
        self.__get_session_id()
        
        result = self.__session_id

        self.__close()

        return result

    def session_exists(self) -> bool:
        '''session이 존재하는지 확인한다.
        ```
        Returns:
            bool: session 존재 여부
        ```'''
        self.__get_session_id(False)
        result = bool(self.__session_id)
        self.__close()

        return result