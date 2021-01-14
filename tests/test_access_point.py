
import googlemaps
from key import GMAPS_KEY

def access_point():

    gmaps = googlemaps.Client(key = GMAPS_KEY)

    # sample cell tower
    celltowers = [{
        "cellId": 49761,
        "locationAreaCode": 26002,
        "mobileCountryCode": 20,
        "mobileNetworkCode": 10
        },
        {
        "cellId": 27111,
        "locationAreaCode": 1009,
        "mobileCountryCode": 204,
        "mobileNetworkCode": 16
        },
        {
        "cellId": 27161,
        "locationAreaCode": 1003,
        "mobileCountryCode": 204,
        "mobileNetworkCode": 16
        }
    ]

    locator = {
    "homeMobileCountryCode": 204,
    "homeMobileNetworkCode": 8,
    "radioType": "lte",
    "carrier": "KPN",
    "considerIp": "true",
    "cellTowers": {}
    }


    response = gmaps.geolocate(204, 8, 'gsm', 'Base/KPN', True, celltowers)
    print(response)

if __name__ == '__main__':
    access_point()
