#!/usr/bin/python3
'''
 * http://www.hobby-werkstatt-blog.de/arduino/357-schrittmotor-28byj48-am-arduino.php
 * mit PCA9685 I2C-PWM und ULN2003 Treiber
 ********************************************************
    stepForward und stepBackward sind auf max. Geschwindigkeit getrimmt. 
    Dazu mussten alle redundanten set_pwm - Aufrufe auskommentiert werden (speedup-faktor: 3.5).
    Das orginale Schrittmuster ist noch gut erkennbar.
 ********************************************************
 * Tech Specs Motor:
 * Betriebsspannung: 5V
 * Phasen: 4
 * Schrittwinkel: 5,625° (64 Schritte/Umdrehung) stimmt nöd...
 * Gleichstromwiderstand : 50 Ω
 * Geräuschpegel: 40 dB
 * Drehmoment: > 34,3mNm
 * Getriebeübersetzung: 1/64
 * Motor-Ø: 28mm
 * Motor Welle: Ø 5mm, Wellenlänge: 8mm
 * Befestigungsloch-Abstand: 35mm
 * Gewicht: 34g
'''
import Adafruit_PCA9685
import time


class Stepper_PCA9685:

    def __init__(self, freq = 1000, MAX = 4095, channel=[4,5,6,7]):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(freq)
        self.MAX = MAX
        self.channel = channel
        self.stop()


    def stop(self):
        for i in range(4):
            self.pwm.set_pwm(self.channel[i],0,0)

    '''
        nice math version, too slow...
    '''
    def __stepForward(self, steps=10, speed=50):
        speed = float(speed)/(1000.0*1000.0)
        for step in range(steps):
            # one step, alternating the electrical field 8 times...
            for i in range(8):    
                print('Step: '+str(step)+', i: '+str(i))
                # PIN1
                val = int(i < 2 or i == 7) 
                print(val)
                self.pwm.set_pwm(self.channel[0],0,val*self.MAX)
                # PIN2
                val = int(i>0 and i < 4)
                print(val)
                self.pwm.set_pwm(self.channel[1],0,val*self.MAX)
                # PIN3
                val = int(i>2 and i < 6)
                print(val)
                self.pwm.set_pwm(self.channel[2],0,val*self.MAX)
                # PIN4
                val = int(i > 4)
                print(val)
                self.pwm.set_pwm(self.channel[3],0,val*self.MAX)

                time.sleep(speed)

    '''
        core movement function (360° ~ 520 steps) 
    '''
    def stepCounterClockwise(self, steps=10, speed=5):   
        self.stop()          
        for step in range(steps):
            #1
            self.pwm.set_pwm(self.channel[0],0,self.MAX)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[2],0,0)
            self.pwm.set_pwm(self.channel[3],0,0)
            self.waitNanos(speed)

            #2
            #self.pwm.set_pwm(self.channel[0],0,self.MAX)
            self.pwm.set_pwm(self.channel[1],0,self.MAX)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[3],0,0)
            self.waitNanos(speed)

            #3
            self.pwm.set_pwm(self.channel[0],0,0)
            #self.pwm.set_pwm(self.channel[1],0,self.MAX)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[3],0,0)
            self.waitNanos(speed)

            #4
            #self.pwm.set_pwm(self.channel[0],0,0)
            #self.pwm.set_pwm(self.channel[1],0,self.MAX)
            self.pwm.set_pwm(self.channel[2],0,self.MAX)
            #self.pwm.set_pwm(self.channel[3],0,0)
            self.waitNanos(speed)

            #5
            #self.pwm.set_pwm(self.channel[0],0,0)
            self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[2],0,self.MAX)
            #self.pwm.set_pwm(self.channel[3],0,0)
            self.waitNanos(speed)

            #6
            #self.pwm.set_pwm(self.channel[0],0,0)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[2],0,self.MAX)
            self.pwm.set_pwm(self.channel[3],0,self.MAX)
            self.waitNanos(speed)
            
            #7
            #self.pwm.set_pwm(self.channel[0],0,0)
            #self.pwm.set_pwm(self.channel[1],0,0)
            self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[3],0,self.MAX)
            self.waitNanos(speed)

            #8
            self.pwm.set_pwm(self.channel[0],0,self.MAX)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[3],0,self.MAX)
            self.waitNanos(speed)
        self.stop()            

    '''
        core movement function (360° ~ 520 steps) 
    '''
    def stepClockwise(self, steps=10, speed=5):   
        self.stop()         
        for step in range(steps):
            #1
            self.pwm.set_pwm(self.channel[3],0,self.MAX)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[1],0,0)
            self.pwm.set_pwm(self.channel[0],0,0)
            self.waitNanos(speed)

            #2
            #self.pwm.set_pwm(self.channel[3],0,self.MAX)
            self.pwm.set_pwm(self.channel[2],0,self.MAX)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[0],0,0)
            self.waitNanos(speed)

            #3
            self.pwm.set_pwm(self.channel[3],0,0)
            #self.pwm.set_pwm(self.channel[2],0,self.MAX)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[0],0,0)
            self.waitNanos(speed)

            #4
            #self.pwm.set_pwm(self.channel[3],0,0)
            #self.pwm.set_pwm(self.channel[2],0,self.MAX)
            self.pwm.set_pwm(self.channel[1],0,self.MAX)
            #self.pwm.set_pwm(self.channel[0],0,0)
            self.waitNanos(speed)

            #5
            #self.pwm.set_pwm(self.channel[3],0,0)
            self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[2],0,self.MAX)
            #self.pwm.set_pwm(self.channel[0],0,0)
            self.waitNanos(speed)

            #6
            #self.pwm.set_pwm(self.channel[3],0,0)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[1],0,self.MAX)
            self.pwm.set_pwm(self.channel[0],0,self.MAX)
            self.waitNanos(speed)
            
            #7
            #self.pwm.set_pwm(self.channel[3],0,0)
            #self.pwm.set_pwm(self.channel[2],0,0)
            self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[0],0,self.MAX)
            self.waitNanos(speed)

            #8
            self.pwm.set_pwm(self.channel[3],0,self.MAX)
            #self.pwm.set_pwm(self.channel[2],0,0)
            #self.pwm.set_pwm(self.channel[1],0,0)
            #self.pwm.set_pwm(self.channel[0],0,self.MAX)
            self.waitNanos(speed)
        self.stop() #make sure to switch engine off...

    '''
        provide a little delay (way shorter than classic time.sleep)
    '''
    def waitNanos(self, x):
        sumsi = 0
        for i in range(x):
            sumsi+=i
        return sumsi

'''
 just for testing
'''
if __name__=="__main__":
    
    stepper = Stepper_PCA9685()
    t0 = time.time()
    stepper.stepClockwise(120,1)
    tx=time.time()-t0

    t0 = time.time()
    stepper.stop()
    tx=time.time()-t0

    print(str(tx)) 

    t0 = time.time()
    stepper.stepCounterClockwise(120,1)
    tx=time.time()-t0
    print(str(tx)) 
'''  
    for i in range(1,10):
        speed=50*i
        t0 = time.time()
        
        tx=time.time()-t0
        print('speed: '+str(speed)+', '+str(tx)) 
        stepper.stop()
    
'''