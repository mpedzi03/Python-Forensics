#
# NLTK QUERY CLASS MODULE
# Python-Forensics
#       No HASP required
#

import os
import sys
import logging
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem import PorterStemmer
from collections import Counter

class classNLTKQuery:
    def textCorpusInit(self, thePath):
        # Validate the path is a directory
        if not os.path.isdir(thePath):
            return "Path is not a Directory"
        # Validate the path is readable
        if not os.access(thePath, os.R_OK):
            return "Directory is not Readable"
        # Attempt to Create a corpus with all .txt files found in Directory
        try:
            self.Corpus = PlaintextCorpusReader(thePath, '.*')
            print "Processing Files:"
            print self.Corpus.fileids()
            print "Please wait...."
            self.rawText = self.Corpus.raw()
            self.tokens = nltk.word_tokenize(self.rawText)
            upperstop = [word.upper() for word in stopwords.words('english')]
            self.tokens_nostop = [t for t in self.tokens if t not in upperstop]
            
                                  
            self.TextCorpus = nltk.Text(self.tokens)
            
            self.TextCorpusNoStop = nltk.Text(self.tokens_nostop)

            self.stemmer = PorterStemmer()
            self.stemmedTokens = [self.stemmer.stem(t.lower()) for t in self.tokens_nostop]
            self.stemmedText = nltk.Text(self.stemmedTokens)
            
            self.PosTaggedCorpus =nltk.pos_tag(self.tokens)
            
        except:
            return "Corpus Creation Failed"

        self.ActiveTextCorpus = True
        return "Success"

    def printCorpusLength(self):
        print
        print "Corpus Text Length: ",
        print len(self.rawText)
    def printTokensFound(self):
        print
        print "Tokens Found: ",
        print len(self.tokens)
    def printVocabSize(self):
        print
        print "Calculating...."
        print "Vocabulary Size: ",
        vocabularyUsed = set(self.TextCorpus)
        vocabularySize = len(vocabularyUsed)
        print vocabularySize
    def printSortedVocab(self):
        print
        print "Compiling..."
        print "Sorted Vocabulary",
        print sorted(set(self.TextCorpus))
    def printCollocation(self):
        print
        print "Compiling Collocations...."
        self.TextCorpus.collocations()
    def searchWordOccurence(self):
        print
        myWord = raw_input("Enter Search Word: ")
        if myWord:
            wordCount = self.TextCorpus.count(myWord)
            print myWord + " occured: ",
            print wordCount,
            print " times"
        else:
            print "Word Entry is Invalid"
    def generateConcordance(self):
        print
        myWord = raw_input("Enter word to Concord: ")
        if myWord:
            self.TextCorpus.concordance(myWord)
        else:
            print "Word Entry is Invalid"
    def generateSimilarities(self):
        print
        myWord = raw_input("Enter seed word: ")
        if myWord:
            self.TextCorpus.similar(myWord)
        else:
            print "Word Entry is Invalid"
    def printWordIndex(self):
        print
        myWord = raw_input("Find first occurence of what Word?: ")
        if myWord:
            wordIndex = self.TextCorpus.index(myWord)
            print "First Occurrence of " + myWord + " is at offset:",
            print wordIndex
        else:
            print "Word Entry is Invalid"
    def printVocabulary(self):
        print
        print "Compiling Vocabulary Frequencies",
        vocabFreqList = self.TextCorpus.vocab()
        print vocabFreqList.items()
    def searchStemmedKeyword(self):
        print
        wordToStem = raw_input("Enter a single token to stem: ")
        wordStemmed = self.stemmer.stem(wordToStem)
        print "The stemmed version of the word you input is " + wordStemmed
        print
        print "Searching Corpus for your word . ."
        if wordStemmed:
            wordCount = self.stemmedText.count(wordStemmed)
            print wordStemmed + " occured: ",
            print wordCount,
            print " times"
        else:
            print "Token entry is invalid"
    def showAllWordsGivenPosTag(self):
        print
        print "(Examples of parts-of-speech: NN, PRP, VB, VBP, CC, JJ, RB, IN)"
        print
        partOfSpeech = raw_input("Enter part-of-speech to filter words out from Corpus: ").upper()
        words = set()
        for wrd, tag in self.PosTaggedCorpus:
            if tag.startswith(partOfSpeech):
                words.add(wrd)
        print words
    def showAllPosTagsGivenWord(self):
        print
        print "(Examples of parts-of-speech: NN, PRP, VB, VBP, CC, JJ, RB, IN)"
        print
        wordEntered = raw_input("Enter a word for which you would like to search parts of speech: ")
        posTags = set()
        for wrd, tag in self.PosTaggedCorpus:
            if wrd == wordEntered:
                posTags.add(tag)
        print posTags
        # ^Have user enter a Word & print out all Part of Speech tags that the word is given in the Corpus.
    def showMostCommonWordsGivenPosTag(self):
        print
        print "(Examples of parts-of-speech: NN, PRP, VB, VBP, CC, JJ, RB, IN)"
        print
        partOfSpeech = raw_input("Enter part-of-speech: ").upper()
        words = []
        for wrd, tag in self.PosTaggedCorpus:
            if tag.startswith(partOfSpeech):
                words.append(wrd)
        c = Counter(words)
        freqList = c.most_common(20)
        print freqList
        # ^Have user enter Part of Speech tag & then print the 20
        # most prevalent words that have the tag.
            

    
