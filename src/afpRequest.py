__author__ = 'xiwen.yxw'

import sys
import os
import urllib2

MAX_AFP_SIZE = 768
AFP_SUFFIX = ".afp"
HTTP_URL = "http://finger.xiami.com/s/single_search?len=768"

def offsetLoop(fileSize):
    yield ((fileSize/4)/8)*4
    yield (4*((fileSize/4)/8))*4
    yield (7*((fileSize/4)/8))*4

def singleRequest(afp):
    tmp_str = str(afp)
    print tmp_str
    headers = {'afp': str(afp)}
    request = urllib2.Request(url = HTTP_URL, headers = headers)
    print request
    print len(afp)
    response = urllib2.urlopen(request)
    res = response.read()
    print res
    return -1

def bufferLoop(afpFile, len):
    for offset in offsetLoop(len):
        afpFile.seek(offset, 0)
        afpBuf = afpFile.read(MAX_AFP_SIZE)
        yield afpBuf

def afpIdLoop(afpName):
    size = os.path.getsize(afpName)
    fp = open(afpName, 'rb')
    for afpBuf in bufferLoop(fp, size):
        yield singleRequest(afpBuf)

def afpFileLoop(afpHome):
    for f in os.listdir(afpHome):
        fName = afpHome+"/" + f
        if not os.path.isfile(fName):
            continue
        if f[-4:] != AFP_SUFFIX:
            continue
        yield fName

def mainLoop(afpHome, outName):
    outFile = open(outName, "w+")
    for f in afpFileLoop(afpHome):
        line = f + ":"
        for id in afpIdLoop(f):
            line += str(id)
            line += "|"
        line += '\n'
        outFile.write(line)
    outFile.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(-1)
    mainLoop(sys.argv[1], sys.argv[2])