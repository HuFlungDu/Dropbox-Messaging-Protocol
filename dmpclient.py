import os
import argparse
import urllib2

parser = argparse.ArgumentParser(description='Dropbox messaging protocol ping server')
parser.add_argument('Dropbox ID', metavar="did", type=int,
                       help='ID of dropbox account to receive data from')
args = parser.parse_args()
did = vars(args)["Dropbox ID"]
messagenum = 0
while True:
    with open("dmp","wb") as dmpfile:
        dmpfile.write("{}\nPING".format(messagenum))
        print "Sent PING"
    while True:
        try:
            data = urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/dmp/dmp".format(did)).read()
            rmessagenum = int(data.split("\n",1)[0])
            assert rmessagenum == messagenum
            message = data.split("\n",1)[1]
            assert message == "PONG"
            messagenum += 1
            print "Received PONG"
            break
        except Exception as e:
            if e == KeyboardInterrupt:
                raise e
            pass
    