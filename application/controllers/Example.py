from system.core.controller import *

bp = Blueprint('Example', __name__)
api = Api(bp)

@api.resource('/')
class Example(Resource):
    def __init__(self):
        pass

    def get(self):
        return {'message': 'Example Page GET'}

    def post(self):
        return {'message': 'Example Page POST'}

    def put(self):
        return {'message': 'Example Page PUT'}

    def delete(self):
        return {'message': 'Example Page DELETE'}