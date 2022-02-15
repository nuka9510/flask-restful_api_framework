import os
from flask import request
from werkzeug.utils import secure_filename
from application import upload_path

class Upload():
    def file_upload(self, name, path = None, *allowed_extensions):
        flag = False
        file = request.files[name]

        if path is None:
            self.upload_path = upload_path
        else:
            self.upload_path = path

        if allowed_extensions:
            extensions = set(allowed_extensions)

            flag = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in extensions
        else:
            flag = True
        
        if flag:
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_path, filename)
            file.save(filepath)
            return {'result': flag,'filename': filename, 'filepath': filepath}
        else:
            return {'result': flag}