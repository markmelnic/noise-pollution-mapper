
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options

def boot(): 
    dv = webdriver.Chrome(executable_path = r"./chromedriver83.exe")
    #dv.minimize_window()
    return dv

# kill the driver
def killb(dv):
    dv.quit()