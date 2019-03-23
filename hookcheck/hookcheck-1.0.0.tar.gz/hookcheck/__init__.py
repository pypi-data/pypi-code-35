import datetime
import hmac
import http
import typing
import time

import flask

_SLACK_REQUEST_TIMESTAMP_HEADER = "X-Slack-Request-Timestamp"
_SLACK_SIGNATURE_HEADER = "X-Slack-Signature"
_TIME_SYNCHRONIZATION_TOLERANCE = datetime.timedelta(minutes=5)

def _slack(slack_secret, request):
	if _SLACK_REQUEST_TIMESTAMP_HEADER not in request.headers:
		return ("No Slack request timestamp was included in the request.", http.HTTPStatus.BAD_REQUEST)
	timestamp_string = request.headers[_SLACK_REQUEST_TIMESTAMP_HEADER]
	if not timestamp_string.isdigit():
		return ("Slack request timestamp header was not a number.", http.HTTPStatus.BAD_REQUEST)
	timestamp = int(timestamp_string)
	if abs(time.time() - timestamp) > _TIME_SYNCHRONIZATION_TOLERANCE.seconds:
		return ("Request timestamp is too old.", http.HTTPStatus.FORBIDDEN)

	if _SLACK_SIGNATURE_HEADER not in request.headers:
		return ("No Slack signature was included in the request.", http.HTTPStatus.BAD_REQUEST)
	sent_hmac_signature = request.headers[_SLACK_SIGNATURE_HEADER]
	calculated_message = ("v0:%s:" % timestamp).encode("utf-8") + request.get_data()
	calculated_hmac_signature = "v0=" + hmac.new(slack_secret, calculated_message, "sha256").hexdigest()
	if not hmac.compare_digest(sent_hmac_signature, calculated_hmac_signature):
		return ("Invalid Slack HMAC signature.", http.HTTPStatus.FORBIDDEN)

	return None

def slack(slack_secret_string):
	slack_secret = slack_secret_string.encode("utf-8")
	def verifier_generator(wrapped_function):
		def verifier() -> typing.Any:
			result = _slack(slack_secret, flask.request)
			if result is not None:
				return result
			return wrapped_function()
		return verifier
	return verifier_generator
