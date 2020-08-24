
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

    # sample wifi access point
    wifiaccess = {
    }

    try:
        loc = gmaps.geolocate('259', 
                            '2', 
                            'lte', 
                            'Moldcell', 
                            True, 
                            list(celltower)
                            )

        print(loc)
    except Exception as e:
        print(e.message)
