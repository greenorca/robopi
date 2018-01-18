#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from datetime import datetime

# HTTPRequestHandler class
# accepts GET requests like http://localhost:8080/?id=1&temp=21.2&humi=53
# and logs the data temporarilly (until server is shut down)
# accepts GET requests like http://localhost:8080/info to display received data
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  requests = []
  data = []

  # GET
  def do_GET(self):

        # Parse out the arguments.
        # The arguments follow a '?' in the URL. Here is an example:
        #   http://example.com?arg1=val1
        args = {}
        idx = self.path.find('?')
        if idx >= 0:
            args = urlparse(self.path)

        # log the request
        self.requests.append(self.path)

        # display data
        # print("Logging: "+self.path)
        if self.path == '/info' or self.path == '/info/':
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head><meta charset='utf-8'></head><body>","utf8"))
            # Send message back to client
            message = "<h2>Data logger visualization</h2>"
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))

            self.wfile.write(bytes("<div style='width:40%;float:left;display:inline-block;border:1px solid #666; padding: 5px 10px; margin: 5px'>","utf8"))
            self.wfile.write(bytes("<h3>Request history</h3>", "utf8"))

            self.wfile.write(bytes("<ul style='list-style:none'>","utf8"))

            for x in self.requests:
                self.wfile.write(bytes("<li>"+x+"</li>","utf8"))

            self.wfile.write(bytes("</ul>","utf8"))
            self.wfile.write(bytes("</div>","utf8"))
            self.wfile.write(bytes("<div style='width:40%;float:left;display:inline-block;border:1px solid #666;padding: 5px 10px; margin: 5px'>","utf8"))
            self.wfile.write(bytes("<h3>Data received: </h3>", "utf8"))
            self.wfile.write(bytes("<table>","utf8"))
            self.wfile.write(bytes("<tr><th>Time</th><th>ID</th><th>Temperature</th><th>Humidity</th></tr>","utf8"))

            for x in self.data:
                self.wfile.write(bytes("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".
                    format(x[0],x[1],x[2],x[3]),"utf8"))

            self.wfile.write(bytes("</ul>","utf8"))
            self.wfile.write(bytes("</div>","utf8"))
            self.wfile.write(bytes("</body></html>", "utf8"))

        else:
            # Send response status code
            self.send_response(200)
            self.requests.append(self.path)

            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()

            isGoodQuery = True
            temp=0
            my_id=0
            humi=0

            for x in args.query.split('&'):
                keyValues = x.split("=")
                if keyValues[0] == "id":
                    my_id = int(keyValues[1])
                elif keyValues[0] == "temp" or keyValues[0]== "temperature":
                    temp = float(keyValues[1])
                elif keyValues[0]== "humi" or keyValues[0]== "humidity":
                    humi = keyValues[1]
                else:
                    isGoodQuery = False
                    break

            if isGoodQuery:
                self.data.append(['{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
                                  my_id,temp,humi])
                self.wfile.write(bytes("OK","utf8"))
            else:
                self.wfile.write(bytes("invalid parameters: "+args.query, "utf8"))

        return

def start():
  print('starting server...')
  # Server settings, listens on all ip addresses assigned to the computer
  # Choose port 8080,
  # for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  print('server started, exit with CTRL+c')
  httpd.serve_forever()


if __name__ == "__main__":
    # execute only if run as a script
    start()