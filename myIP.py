#Check public IP of DHCP service and notify once IP changed and update IP stored file
#create file myCurrentIP.txt in the python script directory
#Email Alert:  Make sure SENDER email is status 'Less secure app access' = "ON" https://myaccount.google.com/lesssecureapps?

from bot import telegram_chatbot
import urllib.request
import time
import smtplib
import os
import os.path
from os import path
from shutil import copyfile

# Defining Base Path
basePath = os.path.dirname(os.path.abspath(__file__))

# How do you want to be alerted?
alert_method = 'both' # Options: both / telegram / email

# Email Alert Details Gmail.
SENDER = "SENDER EMAIL HERE"
PASS = "SENDER PASSWORD HERE"
RECIVER = "RECIVER EMAIL HERE"

# Set telegram chat id
TELEGRAM_CHAT_ID = "TELEGRAM CHAT ID"

bot = telegram_chatbot(basePath + "/telegram_config.cfg")

# Fetch current IP address from the WWW
FetchURL = urllib.request.urlopen("https://ident.me/")
Data = FetchURL.read()
myIP = Data.decode("utf8")
FetchURL.close()

# Set the current IP file
currentIPFile = basePath + "/myCurrentIP.txt"

# Check if file exists, if not create a file... This file has been .ignored
if path.exists(currentIPFile) == False:
    # Create a copy from the sample file
    copyfile(basePath + "/myCurrentIP.sample", currentIPFile)


FILE = open(currentIPFile, "r")
CurrentIP = FILE.read()

# If IP did not change
if myIP == CurrentIP:
    print("Its all good")

# If IP Changed
elif myIP != CurrentIP:
    oldIP = CurrentIP
    print("IP is different, update is in progress")
    FILE = open(currentIPFile, "w")
    FILE.write(myIP)
    print("IP Updated")
    FILE = open(currentIPFile, "r")
    CurrentIP = FILE.read()
    print("Current IP is " + CurrentIP)
    FILE.close()

    # Send a notification message from TELEGRAM BOT, if option is 'both' or 'telegram'
    if alert_method == 'both' or alert_method == 'telegram':
        bot.send_message("IP updated from " + oldIP + " to " + CurrentIP, TELEGRAM_CHAT_ID)

    # Send a notification message from EMAIL, if option is 'both' or 'email'
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


