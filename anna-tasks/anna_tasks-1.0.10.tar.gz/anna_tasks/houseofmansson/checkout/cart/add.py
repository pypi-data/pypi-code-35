events = [
	{
		"type": "click",
		"target": "#search"
	},
	{
		"type": "send_keys",
		"target": "#search",
		"value": "AB-WTNOTE009"
	},
	{
		"type": "submit",
		"target": "#search"
	},
	{
		"type": "click",
		"target": "a.product-item-photo"
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
