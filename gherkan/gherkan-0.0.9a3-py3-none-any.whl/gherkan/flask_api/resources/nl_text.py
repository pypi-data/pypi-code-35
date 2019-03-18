from flask import jsonify, request, Response
from flask_restful import Resource, reqparse, abort
from .. import API_FSA

class NLText(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("feature", type=str, location='json', default="Robot")
    parser.add_argument("language", type=str, choices=("en", "cs"), required=True, location='json')
    parser.add_argument("background", type=str, location='json')
    parser.add_argument("description", type=str, location='json')
    parser.add_argument("scenarios", type=str, required=True, location='json')

    def get(self):
        """
        response = {
            "language":"en<OR>cz",
            "description": "optional description",
            "context": "context text",
            "scenarios": "scenarios text"
        }
        """
        if API_FSA.canRequestNLText():
            response = API_FSA.requestNLText()
            return response
        else:
            abort(406, message="NL text cannot be requested!")

    def post(self):
        """
        request = {
            "feature": "featurename"
            "language":"en<OR>cs",
            "description": "optional description",
            "context": "context text",
            "scenarios": "scenarios text"
        }
        response pre /nltext POST = {
            "info": "text",
            "lines": ["line1", "line2", ...],
            "error_lines": [5, 3, 11],
            "error_hints": ["Hint for 5", "", "Hint for 11"],
            "errors": true
        }
        """
        args = self.parser.parse_args()

        try:
            response = API_FSA.receiveNLText(args)
        except Exception as error:
            abort(406, message=error)
        else:
            return response
