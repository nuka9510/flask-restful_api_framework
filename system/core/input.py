import ast, re
from flask_restful import reqparse

class Input():
    def __init__(self):
        self.input = reqparse.RequestParser()

    def arg(self, name, arg_type):
        try:
            self.input
        except AttributeError:
            self.input = reqparse.RequestParser()

        self.input.add_argument(name, type=arg_type)
        self.args = self.input.parse_args()

        if arg_type is str:
            self.args[name] = str(self.args[name])

            if re.search("(\[{0,1}\{\"(\w|\d)+\":|\[(\d+|\"(\w|\d)+\")(,(\d+|\"(\w|\d)+\"))*\])", self.args[name]):
                self.json_convert(name)
                return ast.literal_eval(self.args[name])
            else:
                return self.args[name]
        else:
            return self.args[name]

    def json_convert(self, name):
        self.args[name] = self.args[name].replace('\"', '\'')
        self.args[name] = re.sub('(:)null(,|\})', r'\1None\2', self.args[name])
        self.args[name] = re.sub('(:)true(,|\})', r'\1True\2', self.args[name])
        self.args[name] = re.sub('(:)false(,|\})', r'\1False\2', self.args[name])