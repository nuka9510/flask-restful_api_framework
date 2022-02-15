import os
from flask import request
from werkzeug.utils import secure_filename
from application import upload_path

class Upload():
    def __init__(self, name, path = None, *allowed_extensions):
        self.file = request.files[name]

        if path is None:
            self.upload_path = upload_path
        else:
            self.upload_path = upload_path

        if allowed_extensions:
            extensions = set(allowed_extensions)

            return '.' in self.file.filename and \
                self.file.filename.rsplit('.', 1)[1].lower() in extensions
        else:
            return True

    def file_upload(self):
        filename = secure_filename(self.file.filename)
        filepath = os.path.join(self.upload_path, filename)
        self.file.save(filepath)
        return {'filename': filename, 'filepath': filepath}