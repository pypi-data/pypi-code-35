events = [
	{
		"type": "click",
		"target": "#search"
	},
	{
		"type": "send_keys",
		"target": "#search",
		"value": "XA-123"
	},
	{
		"type": "submit",
		"target": "#search"
	},
	{
		"type": "click",
		"target": "a.product-image"
	},
	{
		"type": "click",
		"target": ".required-entry",
		"required": False
	},
	{
		"type": "click",
		"target": {"type": "xpath", "value": "//select[starts-with(@id, 'attribute')]/option[@value='1217']"},
		"required": False
	},
	{
		"type": "click",
		"target": ".add-to-cart"
	}
]

assertions = [
	{
		"type": "current_url",
		"is": "https://www.buildor.se/checkout/cart/"
	},
	{
		"type": "element_exists",
		"target": "a.btn-remove"
	}
]
