events = [
	{
		"type": "click",
		"target": "#search"
	},
	{
		"type": "send_keys",
		"target": "#search",
		"value": "Gel Polish"
	},
	{
		"type": "submit",
		"target": "#search"
	},
	{
		"type": "click",
		"target": ".tocart"
	}
]
assertions = [
	{
		"type": "element_exists",
		"target": ".message-success"
	}
]
