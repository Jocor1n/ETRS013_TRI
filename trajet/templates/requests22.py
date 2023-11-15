import requests


base_url = "https://api.openchargemap.io/v3/poi/"
parameters = {
    "countrycode": "FR",  # For France
    "latitude": 45.7640,
    "longitude": 4.8357,
    "distance": 10,
    "output": "json",
    "maxresults": 10,  # You might want to increase this if allowed
    "key": "e32ff9c4-2103-4f38-999c-46a4e48fc933"
}

response = requests.get(base_url, params=parameters)
data = response.json()

locations = [(item["AddressInfo"]["Latitude"], item["AddressInfo"]["Longitude"]) for item in data]

print(locations)
