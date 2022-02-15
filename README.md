# python_restapi_framework

## 사용 라이브러리 (*필수 설치)
* flask
  ```
  $ pip install -U Flask
  ```
* flask-restful
  ```
  $ pip install flask-restful
  ```
* mysql-connector-python
  ```
  $ pip install mysql-connector-python
  ```
* passlib
  ```
  $ pip install passlib
  ```

## Controller
* application/controllers/Example.py
  ```
  from system.core.controller import *

  bp = Blueprint('Example', __name__[, url_prefix = '/example'])
  api = Api(bp)

  @api.resource('/')
  class Example(Resource):
      def get(self):
          return {'message': 'Example Page GET'}

      def post(self):
          return {'message': 'Example Page POST'}

      def put(self):
          return {'message': 'Example Page PUT'}

      def delete(self):
          return {'message': 'Example Page DELETE'}
  ```
* application/controllers/\__init__.py
  ```
  from system import app
  from . import Example

  app.register_blueprint(Example.bp)
  ```

## Model
* application/models/Example_Model.py
  ```
  from system import Model

  class Example_Model(Model):
      def example(self):
          sql = '''[QUERY]'''
          self.execute(sql)
          res = self.fetchall()
          self.close()
          return res
  ```

### query 실행
  ```
  self.execute([sql], *[data, ...])
  ```
### query 결과
  ```
  self.fetchall()
  or
  self.fetchone()
  ```
### db 연결 해제
  ```
  self.close()
  ```

## Input
  ```
  from system import Input

  input = Input()
  input.arg([param_name], [data_type])
  ```

## Upload
  ```
  from system import Upload

  upload = Upload()
  upload.file_upload([file_name], *[jpg, png, gif, ...], **[upload_path = [upload_path], file_name = [file_name]])
  ```

## Encryption
  ```
  from system import Encryption

  encryption = Encryption()
  encryption.crypt([schema_id], [word], **[salt = [salt], rounds = [rounds:int], ...])
  ```