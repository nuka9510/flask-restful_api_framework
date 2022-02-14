import ast, app, os
from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename

class Controller():
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

    def file(self, name):
        return request.files[name]

    def file_upload_config(self, file, upload_folder = '/', *allowed_extensions):
        app.app.config['UPLOAD_FOLDER'] = upload_folder

        if allowed_extensions:
            extensions = set(allowed_extensions)
            return '.' in file.filename and \
                file.filename.rsplit('.', 1)[1].lower() in extensions
        else:
            return True

    def file_upload(self, file):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'filename': filename, 'filepath': filepath}