import ast, re
from flask_restful import reqparse
from application import config

class Input():
    def __init__(self):
        self.input = reqparse.RequestParser()

    def arg(self, name, **options):
        try:
            self.input
        except AttributeError:
            self.input = reqparse.RequestParser()

        self.input.add_argument(name, **options)
        self.args = self.input.parse_args()

        try:
            if options['action'] == 'append':
                for i in range(len(self.args[name])):
                    if re.search("^(\[|\{)", self.args[name][i]):
                        self.args[name][i] = self.json_str_convert(self.args[name][i])
                        self.args[name][i] = ast.literal_eval(self.args[name][i])
        except KeyError:
            self.args[name] = self.xss_filter(self.args[name])

        return self.args[name]

    def xss_filter(self, val):
        if config['XSS_FILTER']:
            val = re.sub('&', r'&amp;', val)
            val = re.sub('<', r'&lt;', val)
            val = re.sub('>', r'&gt;', val)
            val = val.replace('\\', '/')

        val = re.sub('\"', r'&quot;', val)
        val = re.sub('\'', r'&#x27;', val)

        return val

    def json_str_convert(self, val):
        val = self.xss_filter(val)

        val = re.sub('(\{|\[|, |: )&#x27;', r"\1'", val)
        val = re.sub('&#x27;(\}|\]|,|:)', r"'\1", val)

        return val