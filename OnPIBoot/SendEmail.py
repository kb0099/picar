'''
    Defines SendEmail function.
'''
## SendEmail function
## Should work on python 2.7 and 3.x
## 

def SendEmail(userName, password, recipients, subject, body):
    import smtplib;

    message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (userName, ", ".join(recipients), subject, body);
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587);
        server.ehlo();
        server.starttls();
        server.login(userName, password);
        server.sendmail(userName, recipients, message);
        server.close();
        print ('successfully sent the mail');
    except Exception as err:
        print ("failed to send mail");
        print (err);
        