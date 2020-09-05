
import sys, csv, time
import numpy as np 
import pandas as pd 
import sounddevice as sd

import googlemaps

from key import KEY2
from iploc.loc_tools import ipinfo
from resources.mls_handler import MLS

# format printed output for sound
def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    if int(volume_norm) < 10:
        print ("  %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))
    elif int(volume_norm) < 100:
        print (" %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))

    noise_data.append(volume_norm)


if __name__=='__main__':

    global noise_data

    # get execution start time
    start_time = time.time()
    print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(item.strip() for item in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))

    # write first line if file is empty
    try:
        with open('avg.csv', 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        if data == '':
            with open('avg.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["noise index", "latitude", "longitude", "accuracy", "timeframe"])
    except:
        with open('avg.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["noise index", "latitude", "longitude", "accuracy", "timeframe"])

        # generate datasets
    print("Running MLS checks")
    mls = MLS()
    print("Getting IP information")
    ip = ipinfo()
    mcc_dataset = mls.get_mcc(ip.mcc)
    print("Sorting dataset")
    sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)

    cell_towers = []
    for data in sorted_dataset:
        if sorted_dataset.index(data) == 0:
            continue
        if sorted_dataset.index(data) == 10:
            break
        tower = {}
        tower['cellId'] = data[4]
        tower['locationAreaCode'] = data[3]
        tower['mobileCountryCode'] = data[1]
        tower['mobileNetworkCode'] = data[2]
        cell_towers.append(tower)

    locator = {
    "homeMobileCountryCode": sorted_dataset[0][1],
    "homeMobileNetworkCode": sorted_dataset[0][2],
    "radioType": sorted_dataset[0][0],
    "carrier": sorted_dataset[0][8],
    "considerIp": "false",
    "cellTowers": {}
    }

    gmaps = googlemaps.Client(key = KEY2)

    # start collecting data
    while True:
        try:
            noise_data = []
            # collect data for mil timeframe
            with sd.Stream(callback=print_sound):
                sd.sleep(1000)

            # get gps coordinates
            coords = gmaps.geolocate(sorted_dataset[0][1], sorted_dataset[0][2], sorted_dataset[0][0], sorted_dataset[0][8], False, cell_towers)
            lat = coords['location']['lat']
            lng = coords['location']['lng']
            acr = coords['accuracy']

            # process and write average noise data
            with open("avg.csv", "a", newline='') as avg_file:
                avg_writer = csv.writer(avg_file)

                # get the average noise index
                noise_avg = 0
                for nd in noise_data:
                    noise_avg += float(nd)
                    
                noise_avg = str(noise_avg/len(noise_data))

                # write to dataset
                #print(noise_avg + " average for " + str(len(noise_data)) + " values at latitude " + str(lat) + " and longitude " + str(lng) + "\n----------")
                avg_writer.writerow([noise_avg, lat, lng, acr, time.time()])

        except IndexError:
            pass

        except KeyboardInterrupt:
            break

    # print total execution time  
    print("--- %s seconds ---" % (time.time() - start_time))