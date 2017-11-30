#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import shutil

import os, signal
import mimetypes

# global
httpd = None;

CMD_FORWARD     = 38; # up ----- if pressed makes to go forward 
CMD_BACKWARD    = 40; # down --- makes to go  in reverse
CMD_LEFT        = 37; # left --- left turn
CMD_RIGHT       = 39; # right -- right turn
CMD_STOP        = 83; # s     -- sets speed to ZERO
CMD_ACCELERATE  = 90; # z    --- increases speed
CMD_DECELERATE  = 88; # x      --- decreases speed
CMD_TERMINATE   = 84; # terminatese the whole server, emergency stop measure

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
                output = None;
                output = '{"result": "status"}';
               
                if(cmd == CMD_FORWARD):
                    output = '{"result": "CMD_FORWARD"}';    # move forward , should do IPC or threading or what?
                elif (cmd == CMD_BACKWARD):
                    output = '{"result": "CMD_BACKWARD"}';
                    pass;    
                elif(cmd == CMD_ACCELERATE):
                    output = '{"result": "CMD_ACCL"}';
                    pass;  
                elif(cmd == CMD_DECELERATE):
                    output = '{"result": "CMD_DECL"}';
                    pass;
                elif(cmd == CMD_LEFT):
                    output = '{"result": "CMD_LEFT"}';
                    pass;
                elif(cmd == CMD_RIGHT):
                    output = '{"result": "CMD_RIGHT"}';
                    pass;
                elif (cmd == CMD_TERMINATE):
                    self.stopped = True;
                    self.wfile.write("closing...");
                    self.server_close()
                    return;
                
                # is better to end the connection first?
                self._set_headers('application/json');
                self.wfile.write(output);
                self.finish();
                self.connection.close();

            else:        
                # skip the leading '/' from filepath
                self.send_file(filepath[filepath.find('/') + 1:]);

        except IOError:
            #self.send_error(404, "<html><body><h1>File not found %s </h1></body></html>" % filepath)
            self.send_file("404.html", 404)

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
        
        
def run(server_class=HTTPServer, handler_class=S, port=8282):
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
        httpd.server_close()
        print("\n\nclosed....\nSuccessfully!");

    #except:
    #    print "address already in use?"
def handler_stop_signals(signum, frame):
    global httpd;
    httpd.shutdown();
    httpd.stopped = True;
    httpd.serve_forever();
    httpd.server_close();
    print("\n\nclosed....\nSuccessfully!");

if __name__ == "__main__":
    from sys import argv

    signal.signal(signal.SIGINT, handler_stop_signals);
    signal.signal(signal.SIGTERM, handler_stop_signals);

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

# end