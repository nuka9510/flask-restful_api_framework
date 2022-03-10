class Header():
    def __init__(self):
        self.__headers = []

    def set(self, key, value):
        self.__headers.append((key, value))

    def get(self, session=None):
        result = self.__headers
        self.__headers = []

        if session:
            result.append(session._set_header())

        return result