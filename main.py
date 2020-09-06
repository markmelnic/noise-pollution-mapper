
import sys, csv, time
import numpy as np 
import pandas as pd 
import sounddevice as sd

import googlemaps

from key import KEY2
from iploc.loc_tools import ipinfo
from resources.mls_handler import MLS

# breaker exception
class Breaker(Exception):
    pass

# format printed output for sound
def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    if int(volume_norm) < 10:
        print ("  %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))
    elif int(volume_norm) < 100:
        print (" %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))

    noise_data.append(volume_norm)

def tower_yielder(dataset):
    for data in dataset:
        if dataset.index(data) == 20:
            break
        else:
            yield data

def closest_towers(dataset):
    cells = []
    for tower in dataset:
        if dataset.index(tower) == 10:
            break
        else:
            cell = {}
            cell['cellId'] = tower[4]
            cell['locationAreaCode'] = tower[3]
            cell['mobileCountryCode'] = tower[1]
            cell['mobileNetworkCode'] = tower[2]
            cells.append(cell)
    return cells

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
                csv_writer.writerow(["noise index", "latitude", "longitude", "accuracy", "timeframe", "cell Id"])
    except:
        with open('avg.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["noise index", "latitude", "longitude", "accuracy", "timeframe", "cell Id"])

        # generate datasets
    print("Running MLS checks")
    mls = MLS()
    print("Getting IP information")
    ip = ipinfo()
    mcc_dataset = mls.get_mcc(ip.mcc)
    print("Sorting dataset")
    sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)

    gmaps = googlemaps.Client(key = KEY2)

    # start collecting data
    while True:
        try:
            for tower in tower_yielder(sorted_dataset):
                print(tower)
                cell = {}
                cell['cellId'] = tower[4]
                cell['locationAreaCode'] = tower[3]
                cell['mobileCountryCode'] = tower[1]
                cell['mobileNetworkCode'] = tower[2]
                try:
                    noise_data = []
                    # collect data for mil timeframe
                    with sd.Stream(callback=print_sound):
                        sd.sleep(1000)

                    # get gps coordinates
                    coords = gmaps.geolocate(tower[1], tower[2], tower[0], tower[8], False, cell)
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
                        avg_writer.writerow([noise_avg, lat, lng, acr, time.time(), cell['cellId']])

                except googlemaps.exceptions.ApiError:
                    sorted_dataset.remove(tower)
                    pass

                except IndexError:
                    pass

                except KeyboardInterrupt:
                    raise Breaker

        except Breaker:
            break

    # print total execution time  
    print("--- %s seconds ---" % (time.time() - start_time))