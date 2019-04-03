events = [
	{
		"type": "hover",
		"target": "#minicart"
	},
	{
		"type": "click",
		"target": "#top-cart-btn-checkout"
	},
	{
		"type": "switch_to",
		"target": ".collector-checkout-iframe"
	},
	{
		"type": "send_keys",
		"target": "#customer-identify--input-email",
		"value": "patrik.pihlstrom@caupo.se"
	},
	{
		"type": "send_keys",
		"target": "#customer-identify--input-phone",
		"value": "0123456789"
	},
	{
		"type": "click",
		"target": "#customer-identify--button-submit"
	},
	{
		"type": "click",
		"target": "#purchase-method-select--button-direct-invoice"
	},
	{
		"type": "click",
		"target": "#purchase-perform-direct-invoice--button-submit"
	},
	{
		"type": "sleep",
		"value": 5
	}
]
assertions = [
	{
		"type": "current_url",
		"in": "https://stage.lillynails.se.caupo.se/collectorcheckout/success?OrderNo="
	}
]
