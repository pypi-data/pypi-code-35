events = [
	{
		"type": "click",
		"target": ".authorization-link"
	},
	{
		"type": "click",
		"target": "a[href^='https://stage.lillynails.se.caupo.se/customer/account/login']"
	},
	{
		"type": "send_keys",
		"target": "#email",
		"value": "patrik.pihlstrom@caupo.se"
	},
	{
		"type": "send_keys",
		"target": "#pass",
		"value": "test1234!"
	},
	{
		"type": "submit",
		"target": "#pass"
	}
]
assertions = [
	{
		"type": "current_url",
		"is": "https://stage.lillynails.se.caupo.se/customer/account/"
	}
]
