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
	"value": "wrong_password_123"
  },
  {
	"type": "submit",
	"target": "#pass"
  }
]
assertions = [
  {
	"type": "element_exists",
	"target": ".message-error"
  }
]
