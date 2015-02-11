import SimpleHTTPServer
import SocketServer
import threading
from random import randint
from os import path, chdir

resources_path = path.dirname(__file__)+'/resources/'

def webserver(directory):
    chdir(directory)
    port = randint(1025, 2**16-1)
    httpd = SocketServer.TCPServer(("localhost", port),
        SimpleHTTPServer.SimpleHTTPRequestHandler)
    # quick hack to stop http request logging
    httpd.RequestHandlerClass.log_message = lambda *args: None
    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.daemon = True
    httpd_thread.start()
    return "http://localhost:%i/" % port
