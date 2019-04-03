events = [
	{
		"type": "scroll_to",
		"target": "#iframe-test-wait"
	},
	{
		"type": "click",
		"target": "#iframe-test-wait"
	},
	{
		"type": "wait",
		"target": "#iframe-test-wait-get"
	}
]
assertions = [
	{
		"type": "element_exists",
		"target": "#iframe-test-wait-get"
	}
]
