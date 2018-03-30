import datetime
import serial
import sched
import re
import threading
import fcntl
import struct
import requests
import RPi.GPIO as GPIO
import time


class Wgtscale:
    def __init__(self,raspID,serUsb,serNum,web):
        self.ID = raspID
        self.seri = serial.Serial(serUsb,serNum)
        self.weight = self.seri.readline()
        self.lock = threading.Lock()
        self.web = web
        self.T = threading.Timer(1.0, self.PostToWeb)
        self.T.start()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(22,GPIO.OUT)

    def PostToWeb(self):
        with self.lock:
            digial= re.findall(r"[-+]?\d*\.\d+|\d+",self.weight.replace(" ",""))
            Weight = {'TERMINALID': self.ID ,'WEIGHT': digial}
            r = requests.get(self.web,params=Weight)
            print r.text
            GPIO.output(22,GPIO.HIGH)
            time.sleep(.1)
            GPIO.output(22,GPIO.LOW)

    def run(self):
        while True:
            if self.weight != self.seri.readline():
                self.T.cancel()
                self.weight = self.seri.readline()
                print self.weight
                if "ST" in self.weight:
                    self.PostToWeb()
            else:
                if not self.T.is_alive():
                    self.T=threading.Timer(60.0, self.PostToWeb)
                    self.T.start()


