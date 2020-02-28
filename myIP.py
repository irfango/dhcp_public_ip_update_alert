#Check public IP of DHCP service and notify once IP changed and update IP stored file
#create file myCurrentIP.txt in the python script directory
#Email Alert:  Make sure SENDER email is status 'Less secure app access' = "ON" https://myaccount.google.com/lesssecureapps?


import urllib.request
import time
import smtplib

#Email Alert Details Gmail.
SENDER = "SENDER EMAIL HERE"
PASS = "SENDER PASSWORD HERE"
RECIVER = "RECIVER EMAIL HERE"


FetchURL = urllib.request.urlopen("https://ident.me/")
Data = FetchURL.read()

myIP = Data.decode("utf8")
FetchURL.close()
print(myIP)

FILE = open("myCurrentIP.txt", "r")
CurrentIP = FILE.read()
print(CurrentIP)
if myIP == CurrentIP:
    print("Its all good")
elif myIP != CurrentIP:
    print("IP is different, update is in progress")
    FILE = open("myCurrentIP.txt", "w")
    FILE.write(myIP)
    print("IP Updated")
    FILE = open("myCurrentIP.txt", "r")
    CurrentIP = FILE.read()
    #time.sleep(1)
    print("Current IP is " + CurrentIP)
    FILE.close()

    #Email Alert
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(SENDER, PASS)
    subject = 'DHCP Public IP Updated'
    msg = CurrentIP
    message = 'Subject: %s\n\n%s' % (subject, msg)
    server.sendmail(SENDER, RECIVER, message)
    server.quit()
    print("Email Alert Sent!")


