import os
import argparse
import urllib2

parser = argparse.ArgumentParser(description='Dropbox messaging protocol ping server')
parser.add_argument('Dropbox ID', metavar="did", type=int,
                       help='ID of dropbox account to receive data from')
args = parser.parse_args()
did = vars(args)["Dropbox ID"]
oldmessagenum = -1
while True:
    while True:
        try:
            data = urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/dmp/dmp".format(did)).read()
            messagenum = int(data.split("\n",1)[0])
            assert messagenum != oldmessagenum
            message = data.split("\n",1)[1]
            assert message == "PING"
            print "Received PING"
            break
        except Exception as e:
            if e == KeyboardInterrupt:
                raise e
            pass
    with open("dmp","wb") as dmpfile:
        dmpfile.write("{}\nPONG".format(messagenum))
        oldmessagenum = messagenum
        print "Sent PONG"