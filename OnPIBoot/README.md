#Introduction
This repository contains minimal code to perform 2 functions when PI is powered on:
1) Email the IP address of the Raspberry-PI
2) Start the Local Web Server

#Usage
The settings file is not pushed to github. You need to create a file named "config.py" and declare following variables for email account and local webserver settings.

#Application Settings
    - appName     = "PI Boot Notifier"
#Email Account Settings
    - userName    = "MyEmail@gmail.com"
    - password    = "MyPassword"
    - recipients  = ["Recipient1@gmail.com", "Recipient2@gmail.com", "kedarbas@gmail.com"]
#Local Web Server
    - PORT        = 2000;
    - WEB_ROOT    = "C:\\";

