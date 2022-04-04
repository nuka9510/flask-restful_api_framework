import ast, re
from flask import request
from application import config

class Input():
    def __init__(self):
        '''
        method

        get(name: str[, **options])

        post(name: str[, **options])
        '''

    def __xss_filter(self, val):
        if config['XSS_FILTER']:
            val = re.sub('&', r'&amp;', val)
            val = re.sub('<', r'&lt;', val)
            val = re.sub('>', r'&gt;', val)
            val = val.replace('\\', '/')

        val = re.sub('\"', r'&quot;', val)
        val = re.sub('\'', r'&#x27;', val)

        return val

    def __json_convert(self, val):
        val = self.__xss_filter(val)

        val = re.sub('(\{|\[|, |: )&#x27;', r"\1'", val)
        val = re.sub('&#x27;(\}|\]|,|:)', r"'\1", val)

        return val

    def get(self, name, default=None, action='store'):
        '''
        get(name: str[, **options])

        **options[default=: str|int|..., action: str]
        '''
        result = None

        if action == 'append':
            result = request.args.getlist(name)

            for i in range(len(result)):
                if re.search("^(\[|\{)", result[i]):
                    result[i] = self.__json_convert(result[i])
                    result[i] = ast.literal_eval(result[i])
        elif action == 'store':
            result = request.args.get(name)

            if type(result) == str:
                result = self.__xss_filter(result)

            result = result if result else default

        return result

    def post(self, name, default=None, action='store'):
        '''
        post(name: str[, **options])

        **options[default=: str|int|..., action: str]
        '''
        result = None

        if action == 'append':
            result = request.form.getlist(name)

            for i in range(len(result)):
                if re.search("^(\[|\{)", result[i]):
                    result[i] = self.__json_convert(result[i])
                    result[i] = ast.literal_eval(result[i])
        elif action == 'store':
            result = request.form.get(name)

            if type(result) == str:
                result = self.__xss_filter(result)

            result = result if result else default

        return result