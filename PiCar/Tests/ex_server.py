#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import shutil

import os, signal
import mimetypes

from ex_shared_data import SD;

import json

# global
httpd = None;

class S(BaseHTTPRequestHandler):
    allow_reuse_address = True

    def _set_headers(self, mime_type='text/html', code=200):
        self.send_response(code)
        self.send_header('Content-type', mime_type)
        self.end_headers()

    def do_GET(self):
        #global httpd;
        try:            
            filepath = self.path;
            #print filepath;
            #print "======================================================"
            if(filepath == "/"):  
                self.send_file("index.html");

            elif (filepath.startswith("/cmd")):
                cmd = int(filepath[5:]);          # catches string after "/cmd/"  
                #output = None;
                #output = '{"result": "status"}';
                SD.command_list.put(cmd);

                self._set_headers('application/json');

                if (cmd == 84): # CMD_TERMINATE
                    self.wfile.write('{"result": "closing..."}');
                    self.stopped = True;
                    self.server.shutdown();
                    self.socket.close()
                    print ("server: closing...");
                    return;
                
                # is better to end the connection? # may be use events() to get notified once changes are made?
                self.send_pi_status();
                self.finish();
                self.connection.close();

            else:        
                # skip the leading '/' from filepath
                self.send_file(filepath[filepath.find('/') + 1:]);

        except IOError:
            #self.send_error(404, "<html><body><h1>File not found %s </h1></body></html>" % filepath)
            self.send_file("404.html", 404)

    def send_pi_status(self):        
        self.wfile.write(json.dumps(SD.ps));

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>" + post_data)

    def send_file(self, file_name, code=200):
        ''' file_name: relative to os.getcwd() '''
        complete_path       = os.path.join(os.getcwd(), file_name)
        mime_type, y        = mimetypes.guess_type(complete_path)    
        #print "in sendfile: mime_type = %s, y = %s" % (mime_type, y)   
        #print "sending.... %s" % complete_path
        with open(complete_path, 'rb') as content:
            self._set_headers(mime_type, code)    # placing header here will help to handle 404
            shutil.copyfileobj(content, self.wfile)
        self.finish(); # supposed to close connection?
        self.connection.close();
        
        
def run_server(server_class=HTTPServer, handler_class=S, port=8003):
    global httpd;
    try:
        server_address = ('', port)
        handler_class.allow_reuse_address = True
        httpd = server_class(server_address, handler_class)
        httpd.allow_reuse_address = True
        httpd.stopped = False
        print ('Starting httpd server . . .', port)
        httpd.serve_forever()

    except KeyboardInterrupt:        
        httpd.stopped = True;
        httpd.shutdown()
        httpd.socket.close()
        print("\n\nclosed....\nSuccessfully!");

    #except:
    #    print "address already in use?"
def handler_stop_signals(signum, frame):
    global httpd;
    httpd.stopped = True;
    httpd.shutdown();
    print("\n\nclosed....\nSuccessfully!");

if __name__ == "__main__":
    from sys import argv

    signal.signal(signal.SIGINT, handler_stop_signals);
    signal.signal(signal.SIGTERM, handler_stop_signals);

    if len(argv) == 2:
        run_server(port=int(argv[1]))
    else:
        run_server()

# end
