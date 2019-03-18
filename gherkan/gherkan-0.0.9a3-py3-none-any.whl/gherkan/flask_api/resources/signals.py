from flask import jsonify, request, Response
from flask_restful import Resource, reqparse, abort
import re
from .. import API_FSA

class Signals(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("language", type=str, choices=("en", "cs"), required=True, location='json')
    parser.add_argument("background", type=str, location='json')
    parser.add_argument("description", type=str, location='json')
    parser.add_argument("scenarios", action="append", required=True, location='json')

    langDirRegex = re.compile("^.*#\s*lang\w*\s*:.+$", re.IGNORECASE | re.MULTILINE)

    def get(self):
        """
        response = {
                "language":"en<OR>cs",
                "background": "background text",
                "description": "optional description",
                "scenarios": [
                    "scenario1 signal text",
                    "scenario2 signal text"
                ]
        }
        """
        # Check if NL text was received and processed
        if API_FSA.canRequestSignal():
            # request signal file
            API_FSA.requestSignal()
        else:
            abort(Response({"Error": {"message": "It is not possible to request a signal file. Most likely no NL text was provided."}}))

    def post(self):
        """
        request = {
                "language": "en<OR>cs",
                "background": "background text",
                "description": "optional description",
                "scenarios": [
                    "scenario1 signal text",
                    "scenario2 signal text"
                ]
        }
        """
        # A signal file arrived
        args = self.parser.parse_args()
        fileText = '\n'.join(args["scenarios"])
        
        # TODO: better text file composition

        if args["background"] is not None:
            fileText = '\n'.join([args["background"], fileText])

        # if self.langDirRegex.search(fileText) is None:
        #     # Add language directive if it is not in the text
        #     fileText = '\n'.join([args["language"], fileText])
            
        try:
            API_FSA.receiveSignal(fileText)
        except Exception as error:
            abort(Response({"Error": {"message": error}}))

        return {"OK": True}