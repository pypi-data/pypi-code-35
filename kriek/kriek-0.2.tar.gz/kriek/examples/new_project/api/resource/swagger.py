from .. import api
from kriek import File

swagger = api.module("swagger", prefix="/doc")

@swagger.route('/')
def doc_index():
    return {"message": "please pay biatch"}, 402

@swagger.route('/download/settings')
def download():
    return File(path='settings.py')
