#!/usr/bin/env python2.7  
# script by Alex Eames http://RasPi.tv/  
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio  
import RPi.GPIO as GPIO 
import time
import os
from subprocess import call

GPIO.setmode(GPIO.BCM)  

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
#LCD_ON = 12
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

 
# Timing constants
E_PULSE = 0.0025
E_DELAY = 0.0025
#E_ON = 5
     
pinBtn = 26
offBtn = 21
#currentState = 0

def main():
	currentState = 0	   
	# Main program block
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
	# GPIO 26 set up as input. It is pulled up to stop false signals  
	GPIO.setup(pinBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(offBtn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
	GPIO.add_event_detect(offBtn, GPIO.RISING, callback=shutdown, bouncetime=200)

	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	time.sleep(1)
	# Initialise display
	lcd_init()
	lcd_string('PI STATUS MONITOR',LCD_LINE_1)
	#handle_output(currentState)
	while 1:
		try:  
			GPIO.wait_for_edge(pinBtn, GPIO.FALLING)  
			currentState = (currentState + 1)%4
			handle_output(currentState)
			print("\nFalling edge detected.")
  
		except KeyboardInterrupt:  
			pass


def handle_output(currentState):
	lcd_init()
#	lcd_string("State: "+str(currentState),LCD_LINE_1)
	if currentState==0:
		msg = os.popen("df -h | grep root | awk '{print $2, $4}'").read()[0:-1]
		lcd_string("Pi: "+str(time.ctime()),LCD_LINE_1)
		lcd_string("Disk free:",LCD_LINE_2)
		lcd_string("/ "+msg,LCD_LINE_3)
		msg = os.popen("df -h | grep usb_store | awk '{print $2, $4}'").read()[0:-1]
		lcd_string("USB "+msg,LCD_LINE_4)
		

	elif currentState==1:
		#cpu_util = os.popen('CPU=`top -bn1 | grep "Cpu(s)" |            sed "s/.*, *\([0-9.]*\)%* id.*/\1/" ')
		msg = os.popen("vcgencmd measure_temp").read()[0:-1]
		lcd_string(msg,LCD_LINE_1)
		lcd_string(" ", LCD_LINE_2)
		lcd_string(" ", LCD_LINE_3)

	elif currentState==3:
		msg=os.popen("free -h | grep Mem | awk '{print $2,$3,$4}'").read()[0:-1]
		lcd_string("Memory Status:",LCD_LINE_1)
		lcd_string("total used free",LCD_LINE_2)
		lcd_string(msg,LCD_LINE_3)
		lcd_string(" ", LCD_LINE_4)
	

def lcd_init():
  # Initialise display  
  lcd_byte(0x33,LCD_CMD) # 110010 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  #lcd_byte(0x02,LCD_CMD) # 000010 Cursor Pos 0
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    time.sleep(E_DELAY)
 
def shutdown(pin):
	call('halt',shell=False)
	lcd_init()
	lcd_string('Bye bye...',LCD_LINE_1)

if __name__ == '__main__':
 
  try:
    main()
    print('setup finished')
    
  except KeyboardInterrupt:
    print('autsch, failed to init')

  finally:
    lcd_init()
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
