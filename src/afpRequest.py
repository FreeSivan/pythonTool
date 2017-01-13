__author__ = 'xiwen.yxw'

import sys
import os

MAX_AFP_SIZE = 768
AFP_SUFFIX = ".afp"

def offset_loop(fileSize):
    yield ((fileSize/4)/8)*4
    yield (4*((fileSize/4)/8))*4
    yield (7*((fileSize/4)/8))*4

def singleRequest(afp, MAX_AFP_SIZE):
    return -1

def bufferLoop(afpFile, len):
    for offset in offset_loop(len):
        afpFile.seek(offset, 0)
        afpBuf = afpFile.read(MAX_AFP_SIZE)
        yield afpBuf

def afpIdLoop(afpName):
    size = os.path.getsize(afpName)
    fp = open(afpName, 'rb')

    for afpBuf in bufferLoop(fp, size):
        yield singleRequest(afpBuf, size)

def afpFileLoop(afpHome):
    for f in os.listdir(afpHome):
        print "f name = " + f
        fName=afpHome+"/" + f
        if not os.path.isfile(fName):
            continue
        tmp = fName[-4:]
        print "tmp = " + tmp
        if f[-4:] != AFP_SUFFIX:
            continue
        print "f name = " + f
        yield f

def mainLoop(afpHome, outName):
    outFile = open(outName, "w+")
    for f in afpFileLoop(afpHome):
        print "f = "+f
        str = "" + f + ":"
        for id in afpIdLoop(f):
            print "id = " + id
            str += id
            str += "|"
        str += '\n'
        outFile.write(str)
    outFile.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(-1)
    mainLoop(sys.argv[1], sys.argv[2])