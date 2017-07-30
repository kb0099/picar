'''
    Defines the SendIP function.
'''

'''
    Sends IP address to an email using details from config module.
'''
def SendIP():
    from SendEmail import SendEmail; 
    from socket import gethostbyname, gethostname, getfqdn;
    from config import appName, userName, password, recipients;
    import datetime;

    SendEmail(userName, password, recipients, appName +  ": " + datetime.datetime.now().isoformat(), gethostbyname(getfqdn()));
