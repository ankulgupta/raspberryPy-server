import BaseHTTPServer
import os,sys
import requests
import google
import sysinfo_pi
import RPi.GPIO as GPIO
import time
from urlparse import parse_qs
PORT_NUMBER = 8080

new_path = None

class req_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    GPIO.setup(11, GPIO.OUT)
    def flick(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  
        return  

    def do_GET(self):
        path = self.path
        if path != '/':
            #curdir = os.path.dirname(__file__)
            params = parse_qs(path[2:])
            q1 = params["lat"][0]
            q2 = params["lon"][0]
            new_path = "www.api.openweathermap.org/data/2.5/weather?"+ "lat=" + q1 + "&lon=" + q2
            
            # sending response
            self.send_response(200)
            self.send_header('Content-type','text/html')

            if (q1 != "0" and q2 != "0"):
                r = requests.get("http://{0}".format(new_path))
                json_data = r.json()
                self.send_header('Content-length',len(data))
                self.end_headers()
                self.wfile.write(json_data)
                flick(11)
            elif (q1 == "0" and q2 == "0"):
                info = sysinfo_pi.init()
                self.wfile.write(info)
                flick(11)

try:
    server = BaseHTTPServer.HTTPServer(("0.0.0.0", PORT_NUMBER),req_handler)
    print "Httpserver on port ", PORT_NUMBER
    server.serve_forever() 
except KeyboardInterrupt:
    print "^C received, abort server operations"
    server.socket.close()