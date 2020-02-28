#Check public IP of DHCP service and notify once IP changed and update IP stored file
#create file myCurrentIP.txt in the python script directory
import urllib.request
import time
import smtplib


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


