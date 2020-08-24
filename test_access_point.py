
import googlemaps
from key import KEY2

def access_point():

    gmaps = googlemaps.Client(key = KEY2)

    # sample cell tower
    celltower = {
        "cellId": 42345,
        "locationAreaCode": 4002,
        "mobileCountryCode": 259,
        "mobileNetworkCode": 2
    }

    locator = {
    "homeMobileCountryCode": 259,
    "homeMobileNetworkCode": 2,
    "radioType": "wcdma",
    "carrier": "Vodafone",
    "considerIp": "true",
    "cellTowers": {
        "cellId": 42345,
        "locationAreaCode": 4002,
        "mobileCountryCode": 259,
        "mobileNetworkCode": 2}
    }

    response = gmaps.geolocate(locator)
    print(response)

if __name__ == '__main__':
    access_point()
