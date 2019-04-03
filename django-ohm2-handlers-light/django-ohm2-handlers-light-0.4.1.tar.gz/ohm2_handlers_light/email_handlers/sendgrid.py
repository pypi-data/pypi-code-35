from ohm2_handlers_light.definitions import EmailHandler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

class Sendgrid(EmailHandler):


	def __init__(self, *args, **kwargs):
		self.API_KEY = kwargs.pop("key")
		super(Sendgrid, self).__init__(*args, **kwargs)


	def send(self, tries = 2, delay = 0.1):
		message = Mail(
			from_email = self.from_email,
			to_emails = self.to_email,
			subject = self.subject,
			html_content = self.content,
		)
		for x in range(tries):
			try:
				sg = SendGridAPIClient(self.API_KEY)
				res = sg.send(message)
			except Exception as e:
				res = None
			
			if res != None and (res.status_code == 200 or res.status_code == 202):
				return True
			
			time.sleep(delay)