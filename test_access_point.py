
import googlemaps
from key import KEY2

def access_point():

    gmaps = googlemaps.Client(key = KEY2)

    # sample cell tower
    celltower = {
        "cellId": 49761,
        "locationAreaCode": 212,
        "mobileCountryCode": 204,
        "mobileNetworkCode": 8
        }

    celltowers = []

    locator = {
    "homeMobileCountryCode": 204,
    "homeMobileNetworkCode": 8,
    "radioType": "lte",
    "carrier": "KPN",
    "considerIp": "true",
    "cellTowers": {}
    }


    response = gmaps.geolocate(204, 8, 'lte', 'KPN', False, celltower)
    print(response)

if __name__ == '__main__':
    access_point()
