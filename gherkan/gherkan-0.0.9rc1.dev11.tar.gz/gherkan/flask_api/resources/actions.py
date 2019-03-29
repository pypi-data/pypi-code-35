from flask import jsonify, request
from flask_restful import Resource, reqparse
from .. import API_FSA

class Actions(Resource):
    parser = reqparse.RequestParser()

    def get(self, language=''):
        return API_FSA.requestRobotPrograms(language)

    def post(self, language=''):
        API_FSA.receiveRobotPrograms(request.form["data"], language)
        return {"OK": True}

