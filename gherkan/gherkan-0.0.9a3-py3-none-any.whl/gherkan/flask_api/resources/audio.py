from flask import jsonify, request, Response
from flask_restful import Resource, reqparse, abort
import os
from .. import API_FSA

class Audio(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("language", type=str, choices=("en", "cs", "cz"), required=True, location='json')
    parser.add_argument("background", type=str, location='json', default="")
    parser.add_argument("description", type=str, location='json', default="")

    def post(self):
        """
        request = {
            "language": "en",
            "description": "desc text",
            "background", "optional background text"
            }
        E.g.: curl -F file=@nl_audio_file.mp3 -F 'data={"language": "en", "description": "desc text", "background", ""}'  <URI>/audio

        response = {
            "language": "en",
            "description": "desc text",
            "background", "optional background text",
            "transcript": "text extracted from audio"
        }
        """
        args = self.parser.parse_args()
        
        for key, value in request.files.items():
            audioFileName = os.path.join(API_FSA.audioFolder, value.filename)
            value.save(audioFileName)
        try:
            transcript = API_FSA.receiveAudio(audioFileName)
        except Exception as error:
            abort(400, message=error)
        else:
            return {
                "langauge": args["language"],
                "description": args["description"],
                "background": args["background"],
                "transcript": transcript
                }
