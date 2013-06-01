import os
import argparse
import urllib2
import dmp

parser = argparse.ArgumentParser(description='Dropbox messaging protocol ping server')
parser.add_argument('Receive Dropbox ID', metavar="rdid", type=int,
                       help='ID of dropbox account to receive data from')
parser.add_argument('Your Dropbox ID', metavar="ydid", type=int,
                       help='Your dropbox ID')
parser.add_argument('Save path', metavar="path", type=str,
                       help='Path to save file to, a directory')

args = parser.parse_args()
rdid = vars(args)["Receive Dropbox ID"]
ydid = vars(args)["Your Dropbox ID"]
path = vars(args)["Save path"]

if not os.path.isdir(path):
    print "Error: Save path needs to be a directory"
    exit()
try:
    os.remove(os.path.join(dmp.dropbox_folder,"dmp{}".format(rdid)))
except:
    pass

oldmessagenum = -1
filepath = ""
while True:
    messagenum, message = dmp.receive(ydid,rdid)
    print messagenum,message
    if messagenum == oldmessagenum:
        continue
    if message == "Done!":
        print "File successfully downloaded! Saved to: {}".format(filepath)
        break
    if messagenum == 0:
        try:
            filepath = os.path.join(path,os.path.basename(message))
            open(filepath,"w").close()
        except:
            print "Sender sent bad filename"
            break
    else:
        data = urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/{}".format(rdid,message)).read()
        with open(filepath,"ab") as outfile:
            outfile.write(data)

    dmp.send(messagenum,"Received!",rdid)
    oldmessagenum = messagenum

try:
    os.remove(os.path.join(dmp.dropbox_folder,"dmp{}".format(rdid)))
except:
    pass