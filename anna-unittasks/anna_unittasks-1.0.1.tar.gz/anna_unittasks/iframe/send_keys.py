events = [
	{
		"type": "scroll_to",
		"target": "#iframe-test-send-keys"
	},
	{
		"type": "send_keys",
		"target": "#iframe-test-send-keys",
		"value": "iframe_test_send_keys"
	}
]
assertions = [
	{
		"type": "element_exists",
		"target": ".iframe_test_send_keys"
	}
]
