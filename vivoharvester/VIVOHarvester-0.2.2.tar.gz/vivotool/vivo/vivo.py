import requests


class VIVO:
    """docstring for VIVO"""

    def get_query_content(self, objcontent, optype):

        ops = ["describe", "insert", "delete"]
        if not optype or (optype not in ops):
            return ""

        query_content = ""

        if optype == "describe":
            query_content = "DESCRIBE <" + objcontent + ">"
            return query_content

        query_content = "DATA {\n" + \
            "GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {\n"
        query_content += objcontent
        query_content += "}\n}\n"

        if optype == "insert":
            query_content = "INSERT " + query_content
        elif optype == "delete":
            query_content = "DELETE " + query_content

        return query_content

    def request_vivo(self, reqcontent, vivo_endpoint, headers, data, optype):

        ops = ["update", "query"]
        if not optype or (optype not in ops):
            return None

        data[optype] = reqcontent
        response = requests.post(vivo_endpoint, headers=headers, data=data)

        return response
