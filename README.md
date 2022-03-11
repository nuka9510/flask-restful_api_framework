# flask-restful_api_framework

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

  bp = Blueprint('Example', __name__[, url_prefix='/example'])
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
  self.execute(sql[, *data, ...])
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

## Util
* application/utils/Example_Util.py
  ```
  class Example_Util():
    [UTIL_METHOD]
  ```
* application/utils/\__init__.py
  ```
  from .Example_Util import Example_Util as Example_Util
  ```
###
  ```
  from application.utils import Example_Util

  util = Example_Util()

  util.[UTIL_METHOD]
  ```

## Input
  ```
  from system import Input

  input = Input()

  input.arg(name[, **options])
  ```

## Upload
  ```
  from system import Upload

  upload = Upload()

  upload.file_upload(name[, *allowed_extensions][, **options])
  ```
### 파일 업로드
  ```
  upload.file_upload(name[, *allowed_extensions][, **options])
  ```
  * return
  ```
  {
    'result': True, // bool
    'file_name': 'file_name.jpg', // string
    'file_path': '/file_path', //string
    'full_path': '/file_path/file_name.jpg', // string
    'raw_name': 'file_name', // string
    'orig_name': 'file_name', // string
    'file_ext': '.jpg' // string
  }
  ```

## Encryption
  ```
  from system import Encryption

  encryption = Encryption([schema='sha256'])

  encryption.crypt(word[, **options])
  ```

## Session
  ```
  from system import Session

  session = Session()

  session.set(key, value)
  session.get(key)
  session.pop(key)
  session.clear()
  session.close()
  ```

## Header
  ```
  from system import Header

  header = Header()

  header.set(key, value)
  header.get([session=None])
  ```