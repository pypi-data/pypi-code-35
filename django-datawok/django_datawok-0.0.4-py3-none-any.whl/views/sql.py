import psycopg2
from django.conf import settings as project_settings
from rest_framework.response import Response
from rest_framework.views import APIView

from datawok.conf import settings
from datawok.utils.api_auth import TokenAPIAuthentication

database = project_settings.DATABASES[settings.DATABASE]


class SQL(APIView):
    """
    View to process raw read-only SQL queries.
    """

    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = ()

    def post(self, request, format=None):
        """
        Execute a read-only SQL query.
        """
        query = request.data["query"]

        cnn = psycopg2.connect(
            dbname=database["NAME"],
            user=database["USER"],
            password=database["PASSWORD"],
            host=database["HOST"],
            port=database["PORT"],
            options="-c statement_timeout={}".format(settings.QUERY_TIMEOUT),
        )
        cnn.set_session(readonly=True)
        cur = cnn.cursor()

        try:
            cur.execute(query)
        except Exception as e:
            cnn.close()
            return Response("Database query error: {}".format(e).strip(), 500)

        resp = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        output = []
        for rowi, row in enumerate(resp):
            if rowi >= settings.QUERY_LIMIT:
                break

            entry = {}
            for index, column in enumerate(columns):
                entry[column] = row[index]
            output.append(entry)

        cnn.close()

        return Response(output, 200)
