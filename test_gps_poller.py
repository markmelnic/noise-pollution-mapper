
import threading
import time
from gps import *


class GpsPoller(threading.Thread):

   def __init__(self):
       threading.Thread.__init__(self)
       self.session = gps(mode=WATCH_ENABLE)
       self.current_value = None

   def get_current_value(self):
       return self.current_value

   def run(self):
       try:
            while True:
                self.current_value = self.session.next()
                time.sleep(0.2)
       except StopIteration:
            pass

if __name__ == '__main__':

   gpsp = GpsPoller()
   gpsp.start()

   while 1:
       time.sleep(5)
       print(gpsp.get_current_value()) 