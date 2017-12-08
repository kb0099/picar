''' 
Scripts to run on Raspberry-PI boot. 
'''
from StartServer import StartServer;
from SendIP import SendIP;

# Email the IP address and start the web server.
#SendIP();
StartServer();
