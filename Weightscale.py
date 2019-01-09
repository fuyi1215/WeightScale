import datetime
import serial
import sched
import re
import threading
import fcntl
import struct
import requests
import RPi.GPIO as GPIO
import sys, time
import logging

logger = logging.getLogger(__name__)

class Wgtscale:
    def __init__(self,raspID,serUsbs,serNum,web):
        print('start initial')
        self.ID = raspID
        self.weights =["","",""]
        self.usbs = serUsbs
        self.serNum = serNum
        print self.usbs
        self.seri = self.findserialsignal()
        #self.seri = serial.Serial(self.usb,serNum,timeout=3)
        logger.info(self.seri)
        self.weight = self.seri.readline()
        logger.info(str(self.weight))
        self.lock = threading.Lock()
        self.web = web
        self.T = threading.Timer(1.0, self.PostToWeb)
        self.T.start()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(22,GPIO.OUT)
        GPIO.output(22,GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(22,GPIO.LOW)
        print('finish initial')

    def findserialsignal(self):
        for usb in self.usbs:
            try:
                print usb
                return serial.Serial(usb,self.serNum,timeout=3) 
                break
            except:
                if usb == 'end':
                    logger.info("lost seri signal")
                    #raise
                    #exit()
        
    def PostToWeb(self):
        try:
            with self.lock:
                digial= re.findall(r"[-+]?\d*\.\d+|\d+",self.weight.replace(" ",""))
                Weight = {'TERMINALID': self.ID ,'WEIGHT': digial}
                r = requests.get(self.web,params=Weight,verify=False,timeout=7)
                GPIO.output(22,GPIO.HIGH)
                time.sleep(.1)
                GPIO.output(22,GPIO.LOW)
                print r.text
        except:
            logger.debug('lost connection')
            time.sleep(2)
            raise
                 

    def run(self):
        try:
            self.weight = "0.0"
            while True:
                if self.weights[0] != self.seri.readline():
                    for i,x in enumerate(self.weights):
                        self.weights[i] = self.seri.readline()
                        time.sleep(.15)
                    
                    if self.weights[0] == self.weights[2] and self.weights[0]==self.weights[1]:
                        self.weight = self.seri.readline()
                        print self.weight
                        if "ST" in self.weight and self.weight == self.weights[0] and "+" in self.weight:
                            self.T.cancel()
                            self.PostToWeb()
                            if not "0.0" in self.weight:
                                logger.info('Store:' + self.weight)
                else:
                    if not self.T.is_alive():
                        self.T=threading.Timer(60.0, self.PostToWeb)
                        self.T.start()
        except:
              logger.debug(sys.exc_info()[0])
              print "Unexpected : ", sys.exc_info()[0]
              time.sleep(10)
              self.seri = self.findserialsignal()
              self.run()
                    


