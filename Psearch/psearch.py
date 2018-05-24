import logging
import time
import _psearch

# p_search: Python Word Search
# Author: Michael Pedzimaz
# October 3, 2017
# Version 2.0
# Simple p_search Python program

if __name__ == '__main__':
    PSEARCH_VERSION = '1.0'
    # turn on logging
    logging.basicConfig(filename='pSearchLog.log', level = logging.DEBUG,
                        format = '%(asctime)s %(message)s')
         # Process the Command Line Arguments
    _psearch.ParseCommandLine()

    log = logging.getLogger('main._psearch')
    log.info("p_search started")

        # Record the Starting Time
    startTime = time.time()
        # Begin reading 
    searchWords, baTarget = _psearch.ReadData()
    
        # Perform Keyword Search
    if _psearch.gl_args.searchWordsSuffix == True:
        _psearch.SearchWordsSuffix(searchWords, baTarget)    
    else:
        _psearch.SearchWords(searchWords, baTarget)
    
    

        # Record the Ending Time
    endTime = time.time()
    duration = endTime - startTime

    logging.info('Elapsed Time: '+ str(duration) + 'seconds')
    logging.info('')

    logging.info('Program Terminated Normally')
