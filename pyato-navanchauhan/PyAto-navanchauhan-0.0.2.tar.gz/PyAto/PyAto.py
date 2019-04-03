import requests

#We set the headers globally as the header remains the same for almmost all requests
def setAPIKey(secret):
	apikey = secret
	global headers
	headers = {
    'Accept': 'application/json',
    'user-key': apikey,
	}


# Get Categories Function

def getCategories():
	response = requests.get('https://developers.zomato.com/api/v2.1/categories', headers=headers)
	return response.json()

# Get Cities function. Only takes City Name. Returns JSON

def getCities(name):
	params = (('q', name),)
	response = requests.get('https://developers.zomato.com/api/v2.1/cities', headers=headers, params=params)
	return response.json()['location_suggestions'][0]

# Get Collections Function. Only takes City ID. Returns JSON

def getCollections(city_id):
	params = (('city_id', city_id),)
	response = requests.get('https://developers.zomato.com/api/v2.1/collections', headers=headers, params=params)
	return response.json()

# Get Cuisines Function. Only takes City ID. Returns JSON

def getCuisines(city_id):
	params = (('city_id', city_id),)
	response = requests.get('https://developers.zomato.com/api/v2.1/cuisines', headers=headers, params=params)
	return response.json()

# Get Establishments Function. Only takes City ID. Returns JSON	

def getEstablishments(city_id):
	params = (('city_id', '1'),)
	response = requests.get('https://developers.zomato.com/api/v2.1/establishments', headers=headers, params=params)
	return response.json()

# Geocoding Function. Takes Latitude and Longitude. Returns JSON

def getGeocode(lat, lon):
	params = (('lat', lat),('lon', lon),)
	response = requests.get('https://developers.zomato.com/api/v2.1/geocode', headers=headers, params=params)
	return response.json()

# Gets the City ID, Takes City Name and returns integer

def getCityID(name):
	params = (('q', name),)
	response = requests.get('https://developers.zomato.com/api/v2.1/cities', headers=headers, params=params)
	return response.json()['location_suggestions'][0]['id']
