class Header():
    def __init__(self):
        '''
        method

        set(key: str, value: str|int|...)

        get([session=None: class Session()])
        '''
        self.__headers = []

    def set(self, key, value):
        '''
        set(key: str, value: str|int|...)

        header에 key, value를 담는다.
        '''
        self.__headers.append((key, value))

    def get(self, session=None):
        '''
        get([session=None: class Session()])

        header를 가져온다.
        '''
        result = self.__headers
        self.__headers = []

        if session:
            result.append(session._set_header())

        return result