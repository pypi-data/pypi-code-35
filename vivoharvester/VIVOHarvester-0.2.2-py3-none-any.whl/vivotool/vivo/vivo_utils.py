class Vivo:
	"""docstring for ClassName"""
	def __init__(self):
		pass


	def request_vivo(rdfurl, rdf_file, vivo_endpoint, headers, data):

	    query_string = "LOAD <" + rdfurl + "vivouploads/rdf/" + rdf_file + \
	            "> into graph <http://vitro.mannlib.cornell.edu/default/vitro-kb-2>"

	    data["update"] = query_string
	    response = requests.post(vivo_endpoint, headers=headers, data=data)

	    return response
