import argparse
import logging
import os
import sys 

log = logging.getLogger('main._psearch')

#Constants
MIN_WORD = 5    #Minimum word size in bytes
MAX_WORD = 15 #Maximum word size in bytes
PREDECESSOR_SIZE = 32 #Values to print before match found
WINDOW_SIZE = 128          #Total values to dump when match found

def ParseCommandLine():
    parser = argparse.ArgumentParser('Python Search')

    parser.add_argument('-v', '--verbose', help = "enables printing of additional program messages", action = 'store_true')
    parser.add_argument('-k', '--keyWords', type = ValidateFileRead, required = True, help = "specify the file containing search words")
    parser.add_argument('-t', '--srchTarget', type = ValidateFileRead, required = True, help = "specify the target file to search")
    parser.add_argument('-m', '--theMatrix', type = ValidateFileRead, required = True, help = "specify the weighted matrix file") 
    parser.add_argument('-s','--searchWordsSuffix', action = 'store_true', required = False, help = "choose to run the function SearchWordsSuffix" )

    global gl_args
    gl_args = parser.parse_args()
    DisplayMessage("Command line processed: Successfully")

    return 

def ValidateFileRead(theFile):
    # Validate the path is a valid
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')
    # Validate the path is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File not readable')

def DisplayMessage(msg):
    if gl_args.verbose:
        print(msg)

    return

def ReadData():
    searchWords = set()
    # read in the text file with words to search for.
    try:
        fileWords = open(gl_args.keyWords, 'r')
        for line in fileWords:
            searchWords.add(line.strip())
    except:
        log.error('Keyword file failure: ' + gl_args.keyWords)
        fileWords.close()
        sys.exit()

    fileWords.close()

    log.info('Search Words')
    log.info('Input file: ' + gl_args.keyWords)
    log.info(searchWords)

    # read the target file into a byte array
    try:
        targetFile = open(gl_args.srchTarget, 'rb')
        baTarget = bytearray(targetFile.read())
    except:
        log.error('Target file failure: ' + gl_args.srchTarget)
        targetFile.close()
        sys.exit()

    targetFile.close()
    log.info('Target of search:' + gl_args.srchTarget)

    return searchWords, baTarget

def SearchWords(searchWords, baTarget):
    sizeOfTarget = len(baTarget)
    # Post to log
    log.info('Target of Search: '+ gl_args.srchTarget)
    log.info('File Size: '+ str(sizeOfTarget))

    baTargetCopy = baTarget

    wordCheck = class_Matrix()
    # Search Loop
    # Step 1, replace all non characters with zero's

    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if not character.isalpha():
            baTarget[i] = 0

    # Step 2, extract possible words from the bytearray
    # and then inspect the search word list
    # create an empty list of probable not found items.
    
    indexOfWords = []
    cnt = 0

    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if character.isalpha():
            cnt += 1
        else:
            if (cnt >= MIN_WORD and cnt <= MAX_WORD):
                newWord = ""
                for z in range(i-cnt, i):
                    newWord = newWord + chr(baTarget[z])
                newWord = newWord.lower()
                if newWord in searchWords:
                    PrintBuffer(newWord, i-cnt, baTargetCopy, i-PREDECESSOR_SIZE, WINDOW_SIZE)
                    indexOfWords.append([newWord, i-cnt])
                    cnt = 0
                    print
                else:
                    if wordCheck.isWordProbable(newWord):
                        indexOfWords.append([newWord, i-cnt])
                        cnt = 0
                        
            else:
                cnt = 0
    PrintAllWordsFound(indexOfWords)
    return

def SearchWordsSuffix(searchWords, baTarget):
    sizeOfTarget = len(baTarget)
    # Post to log
    log.info('Target of Search: '+ gl_args.srchTarget)
    log.info('File Size: '+ str(sizeOfTarget))

    baTargetCopy = baTarget

    wordCheck = class_Matrix()
    # Search Loop
    # Step 1, replace all non characters with zero's

    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if not character.isalpha():
            baTarget[i] = 0

    # Step 2, extract possible words from the bytearray
    # and then inspect the search word list
    # create an empty list of probable not found items.
    
    indexOfWords = []
    cnt = 0
    for i in range (0, sizeOfTarget):
        character = chr(baTarget[i])
        if character.isalpha():
            cnt += 1
        else:
            if (cnt >= MIN_WORD and cnt <= MAX_WORD):
                newWord = ""
                for z in range (i-cnt, i):
                    newWord = newWord + chr(baTarget[z])
                    newWord = newWord.lower()
                    for w in searchWords:
                        if newWord.endswith(w):
                            indexOfWords.append([w, i-cnt])
                            PrintBuffer(newWord, i-cnt, baTargetCopy, i-PREDECESSOR_SIZE, WINDOW_SIZE)
                            cnt = 0
                            print
                        else:
                            if wordCheck.isWordProbable(newWord):
                                indexOfWords.append([newWord, i-cnt])
                                cnt = 0
            else:
                cnt = 0
    
   
    PrintAllWordsFound(indexOfWords)
    return

    # Print Hexidecimal / ASCII Page Heading
def PrintHeading():
    print ("Offset   00  01  02  03  04  05  06  07  08  09  0A  0B  0C  0D  0E  0F    ASCII")
    print ("------------------------------------------------------------------------------------------------------------")
    return

# Print Buffer
# Prints Buffer contents for words that are discovered
# Parameters; 1) Word found 2) Direct Offset to beginning of the word
# 3) buff the bytearray holding the target 4) offset starting position in the buffer for printing
# 5) hexSize. size of hex display windows to print

def PrintBuffer(word, directOffset, buff, offset, hexSize):
    print "Found: "+ word + " At Address: ",
    print "%08x " % (directOffset)
    PrintHeading()
    for i in range(offset, offset+hexSize, 17):
        for j in range(0,17):
            if (j==0):
                print "%08x" %i,
            else:
                byteValue = buff[i+j]
                print "%02x " %byteValue,
        print " ",
        for j in range (0,17):
            byteValue = buff[i+j]
            if (byteValue >= 0x20 and byteValue <= 0x7f):
                print "%c" %byteValue,
            else:
                print '.',
        print
    return
                
# PrintAll Words Found
def PrintAllWordsFound(wordList):
    print "Index of All Words"
    print "---------------------------------"

    wordList.sort()

    for entry in wordList:
        print entry
    print "---------------------------------"
    print

    return

# Class Matrix
# init method, loads the matrix into the set weightedMatrix
# isWordProbable method
#   1) Calculates the weight of the provided word
#   2) Verifies the minimum length
#   3) Calculates the weight for the word
#   4) Tests the word for existence in the matrix
#   5) Returns true of false

class class_Matrix:
    weightedMatrix = set()

    def __init__(self):
        try:
            fileTheMatrix = open(gl_args.theMatrix, 'rb')
            for line in fileTheMatrix:
                value = line.strip()
                self.weightedMatrix.add(int(value,16))
        except:
            log.error('Matrix File Error: '+ gl_args.theMatrix)
            sys.exit()
        finally:
            fileTheMatrix.close()
        return

    def isWordProbable(self, theWord):
        if (len(theWord) < MIN_WORD):
            return False
        else:
            BASE = 96
            wordWeight = 0

            for i in range (4,0,-1):
                charValue = (ord(theWord[i]) - BASE)
                shiftValue = (i-1)*8
                charWeight = charValue << shiftValue
                wordWeight = (wordWeight | charWeight)

                if (wordWeight in self.weightedMatrix):
                    return True
                else:
                    return False
