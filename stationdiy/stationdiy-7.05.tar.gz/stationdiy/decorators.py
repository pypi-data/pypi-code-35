def validate_user(func):

	def wrapper(self, *args, **kwargs):
		
		if self.authenticated:

			func(self, *args, **kwargs )
		else:
			return "[Not Validate User] Maybe you need to execute StationDiY<Instance>.login(username = 'username', password = '****')"

	return wrapper