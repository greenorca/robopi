#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os, sys, time, threading

# Einbindung 0,96 Zoll OLED Display 128x64 Pixel
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

from threading import Timer, Thread

class OledDisplay:

    line1 = 'Line 1'
    line2 = 'Line 2'
    line3 = 'Line 3'
    syncThread = None

    def __init__(self):
        RST = 24

        # Display 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

        # First define some constants to allow easy resizing of shapes.
        self.padding = 2
        self.shape_width = 20
        self.top = self.padding
        self.bottom = self.height-self.padding

        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = self.padding

        # Load default font.
        self.font = ImageFont.load_default() # Wenn keine eigene Schrift vorhanden ist!!!!

        #self.font = ImageFont.truetype("font/DejaVuSansCondensed.ttf", 12) # Schriftart, Schriftgröße
        self.font_b = ImageFont.truetype("font/DejaVuSansCondensed.ttf", 12)
        #self.font_c = ImageFont.truetype("font/DejaVuSansCondensed.ttf", 14)
        #self.font_b = self.font

        # Write one line of text.
        self.draw.text((self.x, self.top+25), 'Start', font=self.font_b, fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()


    def __showMessage(self):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        # Write one line of text.
        self.draw.line((self.x, self.top+14, self.x+self.width, self.top+14), fill=255)
        self.draw.text((self.x, self.top+15), str(self.line1), font=self.font_b, fill=255)
        self.draw.line((self.x, self.top+30, self.x+self.width, self.top+30), fill=255)
        self.draw.text((self.x, self.top+30), str(self.line2), font=self.font_b, fill=255)
        self.draw.line((self.x, self.top+45, self.x+self.width, self.top+45), fill=255)
        self.draw.text((self.x, self.top+45), str(self.line3), font=self.font_b, fill=255)
        self.draw.line((self.x, self.top+60, self.x+self.width, self.top+60), fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()

    def setLine1(self,msg):
        self.line1 = msg
        try:
            self.syncThread.join()
        except:
            pass
        self.syncThread = Thread(target=self.__showMessage)
        self.syncThread.start()
        #self.showMessage()

    def setLine2(self,msg):
        self.line2 = msg
        try:
            self.syncThread.join()
        except:
            pass
        self.syncThread = Thread(target=self.__showMessage)
        self.syncThread.start()

    def setLine3(self,msg):
        self.line3 = msg
        try:
            self.syncThread.join()
        except:
            pass
        self.syncThread = Thread(target=self.__showMessage)
        self.syncThread.start()

if __name__ == "__main__":
    oled = OledDisplay()
    time.sleep(1)
    time.sleep(1)
    oled.setLine1('Huhu, ich bins')
    oled.setLine2('Huhu, ich bin Zeile2')
    time.sleep(0.2)
    oled.setLine3('Huhu, ich bin Zeile3')
