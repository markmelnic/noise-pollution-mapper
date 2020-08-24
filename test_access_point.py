
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
    "homeMobileCountryCode": 204,
    "homeMobileNetworkCode": 10,
    "radioType": "lte",
    "carrier": "KPN",
    "considerIp": "false",
    "cellTowers": {
        "cellId": 60141,
        "locationAreaCode": 6400,
        "mobileCountryCode": 204,
        "mobileNetworkCode": 10}
    }

    response = gmaps.geolocate(locator)
    print(response)

if __name__ == '__main__':
    access_point()
