import os
import stat
import time
import hashlib
import argparse
import csv
import logging
log = logging.getLogger('main._pfish')

def ParseCommandLine():
    parser = argparse.ArgumentParser('Python file system hashing..p-fish')

    parser.add_argument('-v', '--verbose', help='allows progress messages to be displayed', action='store_true')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--md5', help='specifies MD5 algorithm', action='store_true')
    group.add_argument('--sha224', help='specifies SHA224 algorithm', action ='store_true')
    group.add_argument('--sha256', help='specifies SHA256 algorithm', action='store_true')
    group.add_argument('--sha384', help='specifies SHA384 algorithm', action='store_true') 
    group.add_argument('--sha512', help='specifies SHA512 algorithm', action='store_true')

    parser.add_argument('-d', '--rootPath', type=ValidateDirectory, required=True,
                        help="specify the root path for hashing")

    parser.add_argument('-r', '--reportPath', type=ValidateDirectoryWritable, required=True,
                        help="specify the path for reports and logs will be written")

    args = None

    args = parser.parse_args()

    return (args)

def SelectionOfHashingAlgorithm(parseargs):    
    if parseargs.md5:
        hashType = 'MD5'
        log.info('MD5 hashing algorithm initiated..')
    elif parseargs.sha224:
        hashType = 'SHA224'
        log.info('SHA224 hashing algorithm initiated..')
    elif parseargs.sha256:
        hashType = 'SHA256'
        log.info('SHA256 hashing algorithm initiated..')
    elif parseargs.sha384:
        hashType = 'SHA384'
        log.info('SHA384 hashing algorithm initiated..')
    elif parseargs.sha512:
        hashType = 'SHA512'
        log.info('SHA512 hashing algorithm initiated..')
    else:
        hashType="Unknown"
        logging.error('Unknown Hash Type Specified')

    DisplayMessage("Command line processed: Successfully", parseargs)

    return hashType

def WalkPath(enteredArgs, enteredHash):

    processCount=0
    errorCount=0

    oCVS = _CSVWriter(enteredArgs.reportPath+'fileSystemReport.csv',enteredHash)

    log.info('Root Path: ' + enteredArgs.rootPath)

    for root,dirs,files in os.walk(enteredArgs.rootPath):
        for file in files:
            fname = os.path.join(root,file)
            result = HashFile(enteredArgs ,fname, file, oCVS)
            if result is True:
                processCount += 1
            else:
                errorCount += 1
    oCVS.writerClose()

    return(processCount)

def HashFile(enteredArgs, theFile, simpleName, o_result):

    if os.path.exists(theFile):
        if not os.path.islink(theFile):
            if os.path.isfile(theFile):
                try:
                    f = open(theFile, 'rb')
                except IOError:
                    log.warning('Open Failed: '+theFile)
                    return
                else:
                    try:
                            rd = f.read()
                    except IOError:
                            f.close()
                            log.warning('Read Failed: '+theFile)
                            return
                    else:
                        theFileStats = os.stat(theFile)
                        (mode, ino, dev, nlink, uid, gid, size, atime,
                        mtime,ctime) = os.stat(theFile)

                        DisplayMessage("Processing File: " +theFile, enteredArgs)
                        fileSize = str(size)

                        modifiedTime = time.ctime(mtime)
                        accessTime = time.ctime(atime)
                        createdTime = time.ctime(ctime)

                        ownerID = str(uid)
                        groupID = str(gid)
                        fileMode = bin(mode)

                        if enteredArgs.md5:
                            hash=hashlib.md5()
                            hash.update(rd)
                            hexMD5 = hash.hexdigest()
                            hashValue = hexMD5.upper()
                        elif enteredArgs.sha224:
                            hash=hashlib.sha224()
                            hash.update(rd)
                            hexSHA224 = hash.hexdigest()
                            hashValue = hexSHA224.upper()
                        elif enteredArgs.sha256:
                            hash=hashlib.sha256()
                            hash.update(rd)
                            hexSHA256 = hash.hexdigest()
                            hashValue = hexSHA256.upper()
                        elif enteredArgs.sha384:
                            hash=hashlib.sha384()
                            hash.update(rd)
                            hexSHA384 = hash.hexdigest()
                            hashValue = hexSHA384.upper()
                        elif enteredArgs.sha512:
                            hash=hashlib.sha512()
                            hash.update(rd)
                            hexSHA512 = hash.hexdigest()
                            hashValue = hexSHA512.upper()
                        else:
                            log.error('Hash not selected')
                            print "=============================="
                            f.close()
                    
                        o_result.writeCSVRow(simpleName,theFile,fileSize,
                                                    modifiedTime,accessTime,createdTime,
                                                     hashValue,ownerID,groupID,mode)
                        return True
            else:   
                    log.warning('['+repr(simpleName)+', Skipped NOT a File'+']')
                    return False
        else:
                    log.warning('['+repr(simpleName)+',Skipped Link NOT a File'+']')
                    return False
    else:
                    log.warning('['+repr(simpleName)+'. Path does NOT exist'+']')
    return False


def ValidateDirectory(theDir):
    if not os.path.isdir(theDir):
        raise argparse.ArumentTypeError('Directory does not exist')
    if os.access(theDir, os.R_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not readable')
    
def ValidateDirectoryWritable(theDir):
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')

    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

def DisplayMessage(msg, enteredArgs):
    if enteredArgs.verbose:
        print(msg)
        return

class _CSVWriter:

    def __init__(self, fileName, hashType):
        try:
            self.csvFile = open(fileName,'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',',
                                     quoting=csv.QUOTE_ALL)
            self.writer.writerow( ('File','Path','Size','Modified Time','Access Time',
                                   'Created Time', hashType,'Owner','Group','Mode') )
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime,
                    hashVal, own, grp, mod):
        self.writer.writerow( (fileName,filePath,fileSize,mTime,aTime,cTime,
                               hashVal,own,grp,mod) )
    def writerClose(self):
        self.csvFile.close()
        
            
        
        
