#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, SocketServer
import os, sys, time, threading, re
from OledDisplay import OledDisplay
from Car import Car
from threading import Timer, Thread

'''test old class
import SimpleTcpSocketServer
oled=SimpleTcpSocketServer.OledDisplay()
oled.showMessages('Hi World')
'''

server = None
isRunning = True;

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    pattern = None

    def setup(self):
        print('setting up the request handler...')
        #self.display = OledDisplay()
        #self.display.setLine1('Con: '+str(self.client_address[0]))
        self.car = Car()
        # expect messages like 'l65;r63;' 'l-345;r-23;'
        self.pattern = re.compile(r"L(-*\d+);R(-*\d+);")


    def handle(self):
        imUp = True
        while imUp==True:
            # self.request is the TCP socket connected to the client
            data = self.request.recv(100).strip()
            #if len(data)>0:
            print("{} wrote: {}".format(self.client_address[0], data))

            if str(data).startswith('xxx') or len(data)==0:
                imUp = False
                #self.request.sendall(bytes('CIAO...','utf-8'))
                print("Connection closed")
                #self.display.setLine2("disconnected")
                #self.display.setLine3("")

            # just send back the same data, but upper-cased
            else:
                #self.request.send(data.upper())
                ##self.display.setLine2("RAW:" +data.upper())
                match = re.match(self.pattern, str(data))
                if match:
                    leftSpeed = int(match.group(1))
                    rightSpeed = int(match.group(2))
                    self.car.moveCar(leftSpeed, rightSpeed)
                    #self.display.setLine3("L:"+str(leftSpeed)+" R:"+str(rightSpeed))


def killserver():
    try:
        while True:  # wait for a signal, perhaps in a loop?
            time.sleep(0.1)
    except:
        print('going down gracefully')
        server.shutdown()  # graceful quit

if __name__ == "__main__":
    HOST, PORT = "192.168.0.30", 8888

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.allow_reuse_address=1
    server.serve_forever()
    #server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.start()
    print("Server is up: "+str(HOST)+":"+str(PORT))

    #shutdown = Thread(target=killserver)
    #shutdown.start()
