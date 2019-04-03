events = [
	{
		"type": "click",
		"target": "#test-current-url"
	}
]
assertions = [
	{
		"type": "current_url",
		"is": "http://annahub.se:8000/test/switchto"
	},
	{
		"type": "current_url",
		"in": "test/switchto"
	}
]
