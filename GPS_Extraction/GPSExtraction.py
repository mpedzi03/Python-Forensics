# GPS extraction
# Python - Forensics
# No HASP required
import os
import _modEXIF
import _csvHandler
import _commandParser
from classLogging import _ForensicLog
# Offsets into the return EXIFData for
# TimeStamp, Camera Make and Model

TS = 0
Make = 1
Model = 2

# Process the Command Line Arguments
userArgs = _commandParser.ParseCommandLine()

# create a log object
logPath = userArgs.logPath+"ForensicLog.txt"
oLog = _ForensicLog(logPath)

oLog.writeLog("INFO","Scan Started")

csvPath =userArgs.csvPath+"imageResults.csv"
oCSV =_csvHandler._CSVWriter(csvPath)

# define a directory to scan
scanDir = userArgs.scanPath

try:
    picts = os.listdir(scanDir)
except:
    oLog.writeLog("ERROR","Invalid Directory" + scanDir)
    exit(0)

print "Program Start"
print

for aFile in picts:
    targetFile = scanDir+aFile

    if os.path.isfile(targetFile):
        gpsDictionary, EXIFList = _modEXIF.ExtractGPSDictionary (targetFile)
        if (gpsDictionary):
            # Obtain the Lat Lon Alt values from the gpsDictionary
            # Converted to degrees
            # the return value is a dictionary key value pairs
            dCoor = _modEXIF.ExtractLatLonAlt(gpsDictionary)
            lat = dCoor.get("Lat")
            latRef = dCoor.get("LatRef")
            lon = dCoor.get("Lon")
            lonRef = dCoor.get("LonRef")
            alt = dCoor.get("Alt")
            altRef = dCoor.get("AltRef")

            if (lat and lon and latRef and lonRef):
                print str(lat)+','+str(lon)+','+str(alt)

                #write one row to the output file
                oCSV.writeCSVRow(targetFile, EXIFList[Make], EXIFList[Model], EXIFList[TS],  latRef, lat, lonRef, lon, altRef, alt)
                oLog.writeLog("INFO", "GPS Data Calculated for: " + targetFile)
            else:
                oLog.writeLog("WARNING", "No GPS EXIF Data for "+ targetFile)
        else:
            oLog.writeLog("WARNING", "No GPS EXIF Data for " +targetFile)
# Clean up and Close log and CSV File
del oLog
del oCSV
            
