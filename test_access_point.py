
import googlemaps


with open("key.txt", mode='r') as keyfile:
    key = keyfile.read().splitlines()
    keyfile.close()
    
gmaps = googlemaps.Client(key = key[1])
    
celltower = {
    "cellId": 42345,
    "locationAreaCode": 4002,
    "mobileCountryCode": 259,
    "mobileNetworkCode": 2
}

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