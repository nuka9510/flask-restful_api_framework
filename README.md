# my_flask_restapi_project

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

## Controller
### Controller 추가
* application/controllers/Example.py
  ```
  from system.core.controller import *
  from application.models import Example_Model

  bp = Blueprint('Index', __name__)
  api = Api(bp)
  example_model = Example_Model.Example_Model()

  @api.resource('/')
  class Example(Resource):
      def __init__(self):
          self.core = Controller()

      def get(self):
          return {'message': 'Example Page GET'}

      def post(self):
          return {'message': 'Example Page POST'}

      def put(self):
          return {'message': 'Example Page PUT'}

      def delete(self):
          return {'message': 'Example Page DELETE'}
  ```
* application/controllers/__init__.py
  ```
  from application.config.config import app
  from . import Example

  app.register_blueprint(Example.bp)
  ```
### form data 값 가져오기
```
arg([param_name], [data-type])
```
* application/controllers/Example.py
  ```
  ...
  @api.resource('/')
  class Example(Resource):
      def __init__(self):
          self.core = Controller()

      def get(self):
          data = self.core.arg('data', str)
          return {'data': data}
  ```

## Model
### Model 추가
* application/models/Example_Model.py
  ```
  from system.core.model import *

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

### query 실행
```
execute([sql], [*data])
```
* application/models/Example_Model.py
  ```
  def example(self):
      sql = '''[QUERY]'''

      self.db.execute(sql)
      or
      self.db.execute(sql, ('a', 'b', 1, 2))
  ```
### query 결과
```
fetchall()
```
* application/models/Example_Model.py
  ```
  def example(self):
      sql = '''[QUERY]'''

      self.db.execute(sql)
      res = self.db.fetchall()
  ```
```
fetchone()
```
* application/models/Example_Model.py
  ```
  def example(self):
      sql = '''[QUERY]'''

      self.db.execute(sql)
      res = self.db.fetchone()
  ```
### db 연결 해제
```
close()
```
* application/models/Example_Model.py
  ```
  def example(self):
      sql = '''[QUERY]'''

      self.db.execute(sql)
      res = self.db.fetchone()
      self.db.close()
  ```