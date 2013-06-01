import os
import argparse
import urllib2
import dmp

parser = argparse.ArgumentParser(description='Dropbox messaging protocol ping server')
parser.add_argument('Receive Dropbox ID', metavar="rdid", type=int,
                       help='ID of dropbox account to send data to')
parser.add_argument('Your Dropbox ID', metavar="ydid", type=int,
                       help='Your dropbox ID')
parser.add_argument('File', metavar="file", type=str,
                       help='File to send')
def blocksize(size):
    if size[-1].isdigit():
        return int(size)
    else:
        multiplier = 1
        assert size[-1].lower() in "kmg"
        if size[-1].lower() == "k":
            multiplier = 1024
        if size[-1].lower() == "m":
            multiplier = 1024*1024
        if size[-1].lower() == "g":
            multiplier = 1024*1024*1024
        return int(size[:-1])*multiplier
parser.add_argument('-bs, --blocksize', dest="blocksize", type=blocksize,
                       help='Size of blocks to send', default=1024)

args = parser.parse_args()
rdid = vars(args)["Receive Dropbox ID"]
ydid = vars(args)["Your Dropbox ID"]
filepath = vars(args)["File"]
bsize = args.blocksize


if not os.path.isfile(filepath):
    print "File not found"
    exit()

try:
    os.remove(os.path.join(dmp.dropbox_folder,"dmp{}".format(rdid)))
except:
    pass

messagenum = 0
fileoff = 0
maxsize = os.path.getsize(filepath)
try:
    while True:
        if messagenum == 0:
            dmp.send(messagenum,os.path.basename(filepath),rdid)
            while True:
                rmessagenum, message = dmp.receive(ydid,rdid)
                if rmessagenum == messagenum and message == "Received!":
                    break

            messagenum += 1
            continue

        if fileoff >= maxsize:
            dmp.send(messagenum,"Done!",rdid)
            print "Successfully sent message!"
            break

        with open(filepath,"rb")as infile:
            infile.seek(fileoff)
            data = infile.read(bsize)
            fileoff += bsize

        try:
            os.remove(os.path.join(dmp.dropbox_folder,"sendfile{}".format(rdid)))
        except:
            pass

        while True:
            try:
                urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/dmp/{}".format(ydid,"sendfile{}".format(rdid)))
            except:
                break

        with open(os.path.join(dmp.dropbox_folder,"sendfile{}".format(rdid)),"wb") as outfile:
            outfile.write(data)

        while True:
            try:
                urllib2.urlopen("https://dl.dropboxusercontent.com/u/{}/dmp/{}".format(ydid,"sendfile{}".format(rdid)))
                break
            except:
                pass

        dmp.send(messagenum,"dmp/sendfile{}".format(rdid),rdid)
        while True:
            rmessagenum, message = dmp.receive(ydid,rdid)
            if rmessagenum == messagenum and message == "Received!":
                break
        messagenum += 1
finally:
    try:
        os.remove(os.path.join(dmp.dropbox_folder,"sendfile{}".format(rdid)))
    except:
        pass