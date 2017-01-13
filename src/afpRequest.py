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

def dealEachAfp(afpName, outFile):
    size = os.path.getsize(afpName)
    fp = open(afpName, 'rb')
    lst = []

    for afpBuf in bufferLoop(fp, size):
        lst.append(singleRequest(afpBuf, size))
    return lst

def afpFileLoop(afpHome):
    for f in os.listdir(afpHome):
        if not os.path.isfile(f):
            continue
        if f[-4:] != AFP_SUFFIX:
            continue
        yield f

def mainLoop(afpHome, outName):
    outFile = open(outName, "w+")
    for f in afpFileLoop(afpHome):
        dealEachAfp(f, outFile)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(-1)
    mainLoop(sys.argv[1], sys.argv[2])