import tempfile

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from datawok.conf import settings
from datawok.utils.api_auth import TokenAPIAuthentication


class UploadCSVFileView(APIView):
    parser_classes = (FileUploadParser,)
    model = None
    media_type = "text/csv"

    def put(self, request, format=None):
        file_obj = request.data["file"]
        try:
            file_data = file_obj.read().decode(settings.CSV_FILE_ENCODING)
        except Exception as e:
            return Response(
                {"msg": "Error reading or decoding CSV", "error": e},
                status=500,
            )
        with tempfile.TemporaryFile(mode="r+") as tmp:
            try:
                tmp.write(file_data)
                tmp.seek(0)
            except Exception as e:
                return Response(
                    {"msg": "Error loading CSV", "error": e}, status=500
                )
            try:
                self.model.objects.from_csv(tmp)
            except Exception as e:
                return Response(
                    {"msg": "Error updating data.", "error": str(e)},
                    status=500,
                )
        return Response({"msg": "success"}, status=200)


def generate_upload_csv_file_view(model):
    """
    Dynamically generates a viewset for a given model.
    """
    name = "{}UploadCSVFileView".format(model.__name__.title())

    return type(
        name,
        (UploadCSVFileView,),
        {
            "model": model,
            "authentication_classes": (TokenAPIAuthentication,),
            "permission_classes": [],
        },
    )
