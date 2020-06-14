
import csv
import time
import datetime
import numpy as np 
import pandas as pd 
#import geocoder
import sounddevice as sd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from selen_module import *


# get execution start time
start_time = time.time()

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/83.0 Safari/537.36'}
location_link = "https://www.gps-coordinates.net/"

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
      
dv = boot()
dv.get(location_link)
time.sleep(3)
dv.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
for i in range(4):
    dv.find_element_by_css_selector('body').send_keys(Keys.ARROW_UP)
time.sleep(1)

while True:
    noise_data = []
    # collect data for mil timeframe
    with sd.Stream(callback=print_sound):
        sd.sleep(1000)
        
    loc_button = dv.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button")
    loc_button.click()
    
    lat = dv.find_element_by_id("latitude").get_attribute("value")
    lng = dv.find_element_by_id("longitude").get_attribute("value")

    # process and write the average noise
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

killb(dv)

# print total execution time  
print("--- %s seconds ---" % (time.time() - start_time))
'''
if __name__ == '__main__':
    g = geocoder.ip('me')
    print(g.latlng)
'''