from system.core.controller import *

bp = Blueprint('Example', __name__, url_prefix='/example')

@bp.get('/')
def get():
    return {'message': 'Example Page GET'}

@bp.post('/')
def post():
    return {'message': 'Example Page POST'}

@bp.put('/')
def put():
    return {'message': 'Example Page PUT'}

@bp.delete('/')
def delete():
    return {'message': 'Example Page DELETE'}