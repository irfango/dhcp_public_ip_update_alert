#Check public IP of DHCP service and notify once IP changed and update IP stored file
#create file myCurrentIP.txt in the python script directory
#Email Alert:  Make sure SENDER email is status 'Less secure app access' = "ON" https://myaccount.google.com/lesssecureapps?

from bot import telegram_chatbot
import urllib.request
import time
import smtplib
import os

# Defining Base Path
basePath = os.path.dirname(os.path.abspath(__file__))

# How do you want to be alerted?
alert_method = 'both' # Options: both / telegram / email

#Email Alert Details Gmail.
SENDER = "SENDER EMAIL HERE"
PASS = "SENDER PASSWORD HERE"
RECIVER = "RECIVER EMAIL HERE"

TELEGRAM_CHAT_ID = "TELEGRAM CHAT ID"

bot = telegram_chatbot(basePath + "/telegram_config.cfg")

FetchURL = urllib.request.urlopen("https://ident.me/")
Data = FetchURL.read()

myIP = Data.decode("utf8")
FetchURL.close()

currentIPFile = basePath + "/myCurrentIP.txt"

FILE = open(currentIPFile, "r")
CurrentIP = FILE.read()

if myIP == CurrentIP:
    print("Its all good")
elif myIP != CurrentIP:
    oldIP = CurrentIP
    print("IP is different, update is in progress")
    FILE = open(currentIPFile, "w")
    FILE.write(myIP)
    print("IP Updated")
    FILE = open(currentIPFile, "r")
    CurrentIP = FILE.read()
    #time.sleep(1)
    print("Current IP is " + CurrentIP)
    FILE.close()

    # Telegram Bot Sends Message
    if alert_method == 'both' or alert_method == 'telegram':
        bot.send_message("IP updated from " + oldIP + " to " + CurrentIP, TELEGRAM_CHAT_ID)

    #Email Alert
    if alert_method == 'both' or alert_method == 'email':
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


