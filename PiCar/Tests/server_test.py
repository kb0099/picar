#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

import os
import mimetypes

# global
httpd = None;

class S(BaseHTTPRequestHandler):
    allow_reuse_address = True

    def _set_headers(self, mime_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.end_headers()

    def do_GET(self):
        #global httpd;
        try:            
            filepath = self.path;
            print filepath;
            print "======================================================"
            print "filepath = %s" % filepath
            print "compare  = %r" % (filepath == "/close") 
            # mimetype, _ = mimetypes.guess_type(filepath)                
            self._set_headers()
            if(filepath == "/"):
                self.wfile.write("HOME PAGE!")

            elif (filepath == "/close"):
                self.stopped = True;
                self.wfile.write("closing...");
                self.server_close()

            else:
                print "os_join = %s" % (os.path.join('.', filepath))
                f = open(os.path.join('.', filepath));

                self.wfile.write("<html><body><h1>hi!</h1></body></html>")

        except IOError:
            self.send_error(404, "<html><body><h1>File not found %s </h1></body></html>" % filepath)  

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>" + post_data)
        
def run(server_class=HTTPServer, handler_class=S, port=8282):
    global httpd;
    try:
        server_address = ('', port)
        handler_class.allow_reuse_address = True
        httpd = server_class(server_address, handler_class)
        httpd.allow_reuse_address = True
        print 'Starting httpd...'
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.server_close()

    #except:
    #    print "address already in use?"

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()