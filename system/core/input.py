import ast
from flask_restful import reqparse

class Input():
    def __init__(self):
        self.input = reqparse.RequestParser()

    def arg(self, name, arg_type):
        self.input.add_argument(name, type=arg_type)
        args = self.input.parse_args()
        if arg_type is str:
            if '\"' in args[name]:
                return ast.literal_eval(args[name].replace('\"', '\''))
            else:
                return args[name]
        else:
            return args[name]