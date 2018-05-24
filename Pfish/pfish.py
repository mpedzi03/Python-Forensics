import logging
import time
import sys
import _pfish

if __name__=='__main__':

    PFISH_VERSION = '1.0'

    logging.basicConfig(filename='pFishlog.log',level=logging.DEBUG,
                        format='%(asctime)s%(message)s')

    args = _pfish.ParseCommandLine()

    hashType = _pfish.SelectionOfHashingAlgorithm(args)
    startTime=time.time()

    logging.info('')
    logging.info('Welcome to p-fish version'+PFISH_VERSION+'....New Scan Started')
    logging.info('')
    _pfish.DisplayMessage('Welcome to p-fish...version'+PFISH_VERSION, args)

    logging.info('System: '+sys.platform)
    logging.info('Version: '+sys.version)

    filesProcessed = _pfish.WalkPath(args, hashType)

    endTime = time.time()
    duration = endTime-startTime
    logging.info('Files Processed: '+str(filesProcessed) )
    logging.info('Elapsed Time: '+str(duration)+'seconds')
    logging.info('')
    logging.info('Program Terminated Normally')
    logging.info('')

    _pfish.DisplayMessage("Program End", args)
                 
