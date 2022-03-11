import ast, re
from flask_restful import reqparse
from application import config

class Input():
    def __init__(self):
        '''
        method

        arg(name: str[, **options])
        '''
        self.input = reqparse.RequestParser()

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

    def arg(self, name, **options):
        '''
        arg(name: str[, **options])

        **options[type: str|int|..., action: str, location: str, default: str|int|..., ...]

        Flask_RESTful

        reqparse.Argument()

        parameters

        name으로 온 request값을 받는다.
        '''
        self.input.add_argument(name, **options)
        self.args = self.input.parse_args()

        try:
            if options['action'] == 'append':
                for i in range(len(self.args[name])):
                    if re.search("^(\[|\{)", self.args[name][i]):
                        self.args[name][i] = self.__json_convert(self.args[name][i])
                        self.args[name][i] = ast.literal_eval(self.args[name][i])
        except KeyError:
            if type(self.args[name]) == str:
                self.args[name] = self.__xss_filter(self.args[name])

        return self.args[name]