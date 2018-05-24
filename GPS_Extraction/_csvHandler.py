# Writing a Csv file 
import csv
import sys

class _CSVWriter:
    #file will be open for the lifetime of the 
    def __init__(self, fileName):
        try:
            self.csvFile = open(fileName, 'wb')
            print "Opened results file" + fileName
            # creating the writer object
            self.writer = csv.writer(self.csvFile, delimiter = ',',
                                     quoting = csv.QUOTE_ALL)
        except:
            print "ERROR: CSV file failure"
            sys.exit(1)     
        
        # write the header row
        self. writer.writerow(('Image Path', 'Make', 'Model', 'UTC Time',
                               'Lat Ref', 'Latitude', 'Lon Ref', 'Longitude', 'Alt Ref', 'Altitude'))

    def writeCSVRow(self, fileName, cameraMake, cameraModel, utc,
                    latRef, latValue, lonRef, lonValue, altRef, altValue):
        
        #first convert the floating-point lat and lon to strings. 
        latStr = "%.8f" % latValue
        lonStr = "%.8f" % lonValue
        altStr = "%.8f" % altValue
        self.writer.writerow((fileName, cameraMake, cameraModel, utc, latRef, latStr, lonRef, lonStr, altRef, altStr))

    def __del__(self):
        self.csvFile.close()
                             
