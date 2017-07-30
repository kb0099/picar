import sys;
from config import PORT, WEB_ROOT;

def python2x():
    import SimpleHTTPServer
    import SocketServer

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print ("serving at port", PORT)
    httpd.serve_forever()

def python3x():
    import http.server
    import socketserver


    Handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()


def StartServer():
    import os;
    os.chdir(WEB_ROOT)

    if sys.version_info[0] < 3:
        python2x();
    else:
        python3x()
    
