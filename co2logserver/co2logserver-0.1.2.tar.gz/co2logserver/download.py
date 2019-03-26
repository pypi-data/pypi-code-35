# system modules
import json
import re
import io
import urllib

# internal modules
from co2logserver import app
from co2logserver.utils import *
from co2logserver.config import config, database
from co2logserver.authentication import authentication
from co2logserver.exceptions import *

# external modules
from flask import request, render_template, Response, g, send_file
from flask.wrappers import BadRequest


@app.route("/download", methods=["GET"])
@authentication(required="CO2LOGSERVER_DOWNLOAD_REQUIRES_AUTH")
def download(matching_salts={}):
    """
    ``GET`` ``/download`` method with the following parameters:

    format
        one of ``html``, ``csv`` and ``json``. Returns the values in the
        desired format.
    cols
        list of comma-sparated strings. Show only these columns of the database
    number
        integer. Returns so many columns as wanted. If no number is selected it
        will use the default value
    min_COLUMNNAME
        numeric. Return only these rows where ``COLUMNNAME`` is at least this
        high.
    max_COLUMNNAME
        numeric. Return only these rows where ``COLUMNNAME`` is at most this
        high.
    order_by
        COLUMNNAME,<ASC or DESC>. Order the returned rows by ``COLUMNNAME``,
        either ``ASC`` ending or ``DESC`` ending.
    """
    allowedCharacters = "^[a-zA-Z0-9_,.-]*$"

    # CREATE A LIST OF ALL WANTED COLUMNS
    # get the values and save it in a list while it is splitted by ","
    if re.match(allowedCharacters, request.args.get("cols", "*")):
        columnsList = request.args.get("cols", "*").split(",")
        # only use the values wich are in the database header list and the
        # searched one
        columnsList = set(database().header).intersection(columnsList)
    else:
        columnsList = ["*"]

    if len(columnsList) == 0:
        columnsList = ["*"]

    # if there is no correct value or it is larger than the limit in the config
    # we will use the variable from the config number has to be positv and an
    # integer
    limitNumber = request.args.get("number", "")
    if not limitNumber.isdigit() or int(limitNumber) >= config(
        "MAX_LIMIT_OF_ROWS"
    ):
        limitNumber = config("MAX_LIMIT_OF_ROWS")

    # this dictionary holds all the values wich are asked for in the condition
    parametersDict = {"limitValue": limitNumber}

    # create the sql_condition
    # extend the dictionary
    firstValue = True
    sql_condition = ""

    for value in database().header:
        # get only the min and max values which are included in the database
        # header
        minPostValue = request.args.get("min_" + value, "")
        maxPostValue = request.args.get("max_" + value, "")

        # check if the value is not empty and there are no special signs in it
        if minPostValue != "" and re.match(allowedCharacters, minPostValue):
            if firstValue:
                firstValue = False
                # extend the sql condition with the min max values
                sql_condition = " WHERE " + value + " >= " + ":min_" + value
            else:
                sql_condition = (
                    sql_condition + " AND " + value + " >= " + ":min_" + value
                )

            # extend the parameter dictionary
            # Variable und Wert werden dem Dictionary hinzugefuegt
            parametersDict["min_" + value] = minPostValue

        if maxPostValue != "" and re.match(allowedCharacters, maxPostValue):
            if firstValue:
                firstValue = False
                sql_condition = " WHERE " + value + " <= " + ":max_" + value
            else:
                sql_condition = (
                    sql_condition + " AND " + value + " <= " + ":max_" + value
                )

            # Variable und Wert werden dem Dictionary hinzugefuegt
            parametersDict["max_" + value] = maxPostValue

    # ORDER BY <header_value>,<ASC or DESC>
    orderBylist = request.args.get("order_by", "").split(",")
    orderByExpression = ""

    if len(orderBylist) >= 2:
        if orderBylist[0] in database().header and (
            orderBylist[1] == "asc" or orderBylist[1] == "desc"
        ):
            orderByExpression = (
                " ORDER BY " + orderBylist[0] + " " + orderBylist[1] + " "
            )

    fmt = request.args.get("format", "html")
    ctypes = {
        "csv": "text/csv",
        "json": "application/json",
        "html": "text/html",
    }

    def htmlpage(header, rows):
        request_args = request.args.copy()
        request_args.pop("format", None)
        return render_template(
            "datapage.html",
            server={"name": config("NAME")},
            datatable=table2html(header, rows),
            args={"withoutformat": urllib.parse.urlencode(request_args)},
        )

    def csvdownload(header, rows):
        buf = io.BytesIO()
        buf.write(table2csv(header, rows).encode())
        buf.seek(0)
        return send_file(
            buf,
            as_attachment=True,
            attachment_filename="{}-data.csv".format(
                re.sub(r"\W+", "-", config("NAME"))
            ),
            mimetype=ctypes.get("csv"),
        )

    def jsonresponse(header, rows):
        return Response(table2json(header, rows), mimetype=ctypes.get("json"))

    formatters = {"csv": csvdownload, "json": jsonresponse, "html": htmlpage}
    formatter = formatters.get(fmt)
    if formatter:
        cursor = database().select_from_table_with_conditions(
            columnsList=columnsList,
            sql_condition=sql_condition,
            orderByExpression=orderByExpression,
            parameter=parametersDict,
        )
        formatted = formatter(
            header=[c[0] for c in cursor.description], rows=cursor
        )
        return formatted
    else:
        raise BadRequest("Unknown format: '{}'".format(fmt))
