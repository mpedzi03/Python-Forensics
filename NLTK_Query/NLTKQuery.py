#
# NLTK QUERY FRONTexi END
# Python-Forensics
#     No HASP required
#

import sys
import _NLTKQuery

print "Welcome to the NLTK Query Experimentation"
print "Please wait loading NLTK ...."

import _classNLTKQuery

oNLTK = _classNLTKQuery.classNLTKQuery()

print
print "Input full path name where intended corpus file or files are stored"
print "Note: you must enter a quoted string e.g. c:\\simpson\\"
print
userSpecifiedPath = raw_input("Path: ")

# Attempt to create a text Corpus
result = oNLTK.textCorpusInit(userSpecifiedPath)
print "result variable = " + result
if result == "Success":
    menuSelection = -1
    while menuSelection != 0:
        if menuSelection != -1:
            print
            s = raw_input('Press Enter to continue....')
        menuSelection = _NLTKQuery.getUserSelection()

        if menuSelection == 1:
            oNLTK.printCorpusLength()
        elif menuSelection == 2:
            oNLTK.printTokensFound()
        elif menuSelection == 3:
            oNLTK.printVocabSize()
        elif menuSelection == 4:
            oNLTK.printSortedVocab()
        elif menuSelection == 5:
            oNLTK.printCollocation()
        elif menuSelection == 6:
            oNLTK.searchWordOccurence()
        elif menuSelection == 7:
            oNLTK.generateConcordance()
        elif menuSelection == 8:
            oNLTK.generateSimilarities()
        elif menuSelection == 9:
            oNLTK.printWordIndex()
        elif menuSelection == 10:
            oNLTK.printVocabulary()
        elif menuSelection == 11:
            oNLTK.searchStemmedKeyword()
        elif menuSelection == 12:
            oNLTK.showAllWordsGivenPosTag()
        elif menuSelection == 13:
            oNLTK.showAllPosTagsGivenWord()
        elif menuSelection == 14:
            oNLTK.showMostCommonWordsGivenPosTag()
        elif menuSelection == 0:
            print "Goodbye"
            print
        elif menuSelection == -1:
            continue
        else:
            print "unexpected error condition"
            menuSelection = 0
else:
    print "Closing NLTK Query Experimentation"
    
