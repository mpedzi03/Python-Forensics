#MakeMatrix.py

import os
import sys

def main():
    keyWordSet = set()
    
    try:
        fileWords = open(sys.argv[1], 'r')
        for line in fileWords:
            keyWordSet.add(line.strip())
    except:
        fileWords.close()
        sys.exit()
    fileWords.close()
    hexWordSet = set()
    for word in keyWordSet:
        if len(word) < 5:
            continue
        BASE =96
        wordWeight = 0
        for i in range (4,0,-1):
            charValue = (ord(word[i]) - BASE)
            shiftValue = (i-1)*8
            charWeight = charValue << shiftValue
            wordWeight = (wordWeight | charWeight)        
            weightStr = hex(wordWeight)
        hexWordSet.add(weightStr)
                 
    try:
        destinFile = open(sys.argv[2], 'w')
        for line in hexWordSet:
            destinFile.write(line + "\n")
    except:
        destinFile.close()
        sys.exit()
    destinFile.close()
        
            
    return

if __name__ == "__main__":
    main()
