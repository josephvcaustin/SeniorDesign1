import serial
import sys
from time import sleep

class SerialTalker:

    def __init__(self):
        COM = 0
        self.ser = serial.Serial()
        self.initialized = False
        while COM < 4:
            try:
                self.ser = serial.Serial('/dev/ttyACM{}'.format(COM), 115200, timeout=1)
                print("Connected on port {}".format(COM))
                break;
                #self.initialized = self.testComms()
            except Exception as inst:
                COM+=1 # try the next COM port

    def send(self, value):
        self.ser.write('{}'.format(value))
        received = self.ser.readline()
        return received
   
    def testComms(self):
        QUERY = 1000
        ACKNOWLEDGE = 1001
        i = 0
        while i < 5: #retry five times
            received = self.send(QUERY)
            print(received)
            if '1001' in received:
                return True
            else: i+=1
        return False

ser = SerialTalker()
ser.testComms()
