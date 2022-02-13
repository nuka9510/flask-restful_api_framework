from system.core.controller import *
from application.models import Index_Model

bp = Blueprint('Index', __name__)
api = Api(bp)
index_model = Index_Model.Index_Model()

@api.resource('/')
class Index(Resource):
    def __init__(self):
        self.core = Controller()

    def get(self):
        return {'message': 'Index Page GET'}

    def post(self):
        return {'message': 'Index Page POST'}

    def put(self):
        return {'message': 'Index Page PUT'}

    def delete(self):
        return {'message': 'Index Page DELETE'}