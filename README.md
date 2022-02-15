# my_python_restapi_framework

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

  class Example_Model():
      def __init__(self):
          self.db = Model()

      def example(self):
          sql = '''[QUERY]'''
          self.db.execute(sql)
          res = self.db.fetchall()
          self.db.close()
          return res
  ```
* application/models/\__init__.py
  ```
  from .Example_Model import Example_Model as Example_Model
  ```

### query 실행
  ```
  self.db.execute([sql], [*data])
  ```
### query 결과
  ```
  self.db.fetchall()
  or
  self.db.fetchone()
  ```
### db 연결 해제
  ```
  self.db.close()
  ```

## Input
  ```
  from system import Input

  Input().arg([param_name], [data_type])
  ```

## Upload
  ```
  from system import Upload

  Upload().file_upload([file_name], [path = 'upload_path'], *[jpg, png, gif, ...])
  ```

## Encryption
  ```
  from system import Encryption

  Encryption().crypt([schema_id], [word], **[[salt = 'yoursalt'], [rounds = 1000], ...])
  ```