#!/usr/bin/python3

import socketserver
import sys
#from base64 import b64encode
from OledDisplay import OledDisplay
import RPi.GPIO as IO
from Car import Car
'''
threaded socket server, each connection gets its own ThreadedTCPHandler instance
for Python2.7, use socketserver
for Python3.x, use socketserver
'''

from queue import Queue;

queue = Queue(1)

class ThreadedTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    pattern = None

    def setup(self):
        print('setting up the request handler for client '+self.client_address[0])
        self.display = OledDisplay()
        self.display.setLine1('Con: '+str(self.client_address[0]))


    def handle(self):
        imUp = True
        try:
            while imUp==True:
                # self.request is the TCP socket connected to the client
                data = self.request.recv(100).strip()
                data = data.decode('utf-8')
                print("{} wrote: {}".format(self.client_address[0], data))

                if str(data).startswith('xxx') or len(data)==0:
                    imUp = False
                    #self.request.sendall(bytes('CIAO...','utf-8'))
                    print("Connection closed")
                    self.display.setLine2("disconnected")
                    self.display.setLine3("")

                # just put data in queue
                else:
                    if not(queue.full()):
                        queue.put(data)
                        self.display.setLine2("RAW:" +data.upper())
                    else:
                        pass # i don't care

                self.request.sendall(bytes('ACK\n','utf-8'))

        except Exception as ex:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            print("connection terminated: "+str(ex)+" @ line "+str(lineno))

class ThreadedTCPServer(socketserver.ThreadingTCPServer,socketserver.TCPServer):
    pass
    def __init__(self, address_config, handler):
        socketserver.ThreadingTCPServer.__init__(self, address_config, handler)
        self.allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "192.168.43.1", 8888
    HOST, PORT = "192.168.0.61", 8888
    oled = OledDisplay(False)
    oled.setLine1("Starting RoboPi")
    oled.setLine2("IP: "+HOST)

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler)
    ip, port = server.server_address
    car = Car(queue)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    #server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    # server_thread.daemon = True
    #server_thread.start()
    #print("Server loop running in thread: "+server_thread.name)

    IO.setwarnings(False)
    IO.setmode (IO.BCM)
    ledPin = 21
    IO.setup(ledPin,IO.OUT)
    IO.output(ledPin,IO.HIGH)

    try:
        car.start()
        server.serve_forever()
    except Exception as ex:
        oled.setLine1("Autsch...")
        oled.setLine2("X~X")
        print(ex)
    finally:
        print("dying gracefully")
        IO.output(ledPin,IO.LOW)
        server.shutdown()
        server.server_close()
    # Create the server, binding to localhost on port 9999
    # server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    #print("Server is up: "+str(HOST)+":"+str(PORT))
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()
