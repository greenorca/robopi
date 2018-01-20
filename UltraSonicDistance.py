import RPi.GPIO as IO
from threading import Thread
import time

class UltraSonicDistanceSensor:

    pinTrigger = None
    pinEcho = None
    pinDistanceLed = None

    maximumRange = 200; # Maximum range needed
    minimumRange = 0; # Minimum range needed

    tTrigger = 10.0 / (1000*1000)

    def __init__(self, pinTrigger= 22, pinEcho=23, pinLed = 24):
        self.pinTrigger = pinTrigger
        self.pinEcho = pinEcho
        self.pinLed = pinLed

        IO.setwarnings(False)
        IO.setmode (IO.BCM)

        IO.setup(self.pinLed,IO.OUT)
        IO.setup(self.pinTrigger,IO.OUT)
        IO.setup(self.pinEcho,IO.IN)


    def getDistance(self):
        distance = -1
        while distance > 2000 or distance == -1:
            time.sleep(0.1)
            IO.output(self.pinLed, True)
            t0 = 0
            t1 = 0
            IO.output(self.pinTrigger, False)
            time.sleep(0.1)
            IO.output(self.pinTrigger, True)
            time.sleep(self.tTrigger)
            IO.output(self.pinTrigger, False)
            while IO.input(self.pinEcho)==0:
                t0 = time.time()
            while IO.input(self.pinEcho)==1:
                t1 = time.time()

            distance = (t1 - t0) * 17150

        IO.output(self.pinLed, False)
        return round(distance,2)
        pass


if __name__ == "__main__":
    usd1 = UltraSonicDistanceSensor(17,18)
    usd2 = UltraSonicDistanceSensor(22,23)

    i=0
    while i < 100:
        i=i+1
        print("right: "+str(usd1.getDistance()))
        print("left:  "+str(usd2.getDistance()))
        time.sleep(0.2)
