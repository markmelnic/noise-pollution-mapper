
import sys
import csv
import time
import numpy as np 
import pandas as pd 
#import geocoder
import sounddevice as sd
from bs4 import BeautifulSoup

from psl_exec import exec_gps

# get execution start time
start_time = time.time()
print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(item.strip() for item in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    if int(volume_norm) < 10:
        print ("  %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))
    elif int(volume_norm) < 100:
        print (" %.20f" % float(volume_norm), "     ", "|" * int(volume_norm))

    noise_data.append(volume_norm)

global noise_data

# write first line if file is empty
try:
    with open('avg.csv', 'r', newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        data = list(csvReader)
        
    if data == '':
        with open('avg.csv', 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(["noise index", "latitude", "longitude", "timeframe"])
            csvFile.close()
except:
    with open('avg.csv', 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["noise index", "latitude", "longitude", "timeframe"])
        csvFile.close()
      
while True:
    noise_data = []
    # collect data for mil timeframe
    with sd.Stream(callback=print_sound):
        sd.sleep(1000)
    
    coords = exec_gps()
    lat = coords[0]
    lng = coords[1]

    # process and write average noise data
    with open("avg.csv", "a", newline='') as avgFile:
        # generate writer object for changes file
        avgWriter = csv.writer(avgFile)
        noise_avg = 0
        for n in noise_data:
            noise_avg += float(n)
            
        noise_avg = str(noise_avg/len(noise_data))
        print(noise_avg + " average for " + str(len(noise_data)) + " values\n")
        avgWriter.writerow([noise_avg, lat, lng, time.time()])
        avgFile.close()

    #break

# print total execution time  
print("--- %s seconds ---" % (time.time() - start_time))