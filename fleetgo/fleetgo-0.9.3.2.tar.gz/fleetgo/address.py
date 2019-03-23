class Address:
    def __init__(self, json):
        self.country = None
        self.address = None
        self.city = None
        self.postal_code = None
        self.house_number = None

        if (json is not None):
            self.parse_json(json)
    
    def parse_json(self, json):
        self.country = json['Country']
        self.address = json['Address']
        self.city = json['City']
        self.postal_code = json['PostalCode']

    def __str__(self):
        result = ''

        if (self.address is not None and isinstance(self.address, str)):
            result += self.address
        
        if (self.house_number is not None):
            result += ' ' + self.house_number

        if (self.postal_code is not None):
            result += ', ' + self.postal_code

        if (self.city is not None):
            result += ', ' + self.city

        if (self.country is not None):
            result += ', ' + self.country

        result = result.strip(',')
        result = result.strip()

        return result

    def state_attributes(self):
        return {
            'address': self.address,
            'house_number': self.house_number,
            'postal_code': self.postal_code,
            'city': self.city,
            'country': self.country
        }

