#ExtractGPSDictionary(fileName)
#-load an  image file
#-pull out the GPS dictionary if one exists,
#-and construct a new dictionary mapping tag names (not numbers) to values
#-
#ExtractLatLon(gps)
#ConvertToDegrees(coord)

#=======Data Extraction - Python Forensics==========
#Extract GPS Data from EXIF supported Images (jpg.tiff)
#Support Module
import os                                                             #Standard Library OS functions
from classLogging import _ForensicLog        #Abstracted Forensic Logging Class
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
# extract EXIF Data
# input: Full Pathname of the target image
# return: gps Dictionary and selected EXIFData list 
def ExtractGPSDictionary(fileName):
    #open the image file using PIL
    try:
        pilImage = Image.open(fileName)
        EXIFData = pilImage._getexif()
    except:
        return None, None

    # set default values for some image attributes
    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"

    if EXIFData: # this will be a true statement as long as EXIFData does not return 'None"
        gpsDictionary = {} # the dictionary we'll construct
        # iterate through the exif dictionary.
        for tag, value in EXIFData.items():
            # look up the English name for the tag in TAGS.
            tagName = TAGS.get(tag, tag)
            if tagName == 'DateTimeOriginal':
                imageTimeStamp = value
            if tagName == 'Make':
                cameraMake = value
            if tagName == 'Model':
                cameraModel = value
            if tagName == 'GPSInfo': # found the GPS dictionary
                for gpsTag in value:
                    gpsTagName = GPSTAGS.get(gpsTag, gpsTag)
                    gpsDictionary[gpsTagName] = value[gpsTag]
        # the book returns here..
        basicEXIFData = [imageTimeStamp, cameraMake, cameraModel]
        return gpsDictionary, basicEXIFData
    else:
        return None, None,

def ExtractLatLonAlt(gps):
    # to perform the caculation we need at least lat, lon, latRef and lonRef
    if (gps.has_key("GPSLatitude") and gps.has_key("GPSLongitude") and
        gps.has_key("GPSLatitudeRef") and gps.has_key("GPSLongitudeRef")):

        latitude          = gps["GPSLatitude"]
        latitudeRef     = gps["GPSLatitudeRef"]
        longitude       = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]
        altitude = ''   
        default = ''
        if gps.has_key("GPSAltitude"): 
            altitude = gps["GPSAltitude"]
        else:
            gps.setdefault('GPSAltitude', default)
        if gps.has_key("GPSAltitudeRef"):
            altitudeRef    = gps["GPSAltitudeRef"]
        else:
            gps.setdefault("GPSAltitudeRef", default)
            
        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)
        alt = ConvertAltToDegrees(altitude)
            
        # check latitude reference
        # if south of the Equator then lat value is negative
        if latitudeRef =="S":
            lat = 0 - lat
        # check longitude reference
        # if west of the Prime Meridian in
        # Greenwich then the longitude value is negative
        altitudeRef = ''
        if longitudeRef == "W":
            lon = 0 - lon
        if altitudeRef =="1":
            alt = 0 - alt

        gpsCoor = {"Lat": lat, "LatRef": latitudeRef, "Lon": lon, "LonRef": longitudeRef, "Alt": alt, "AltRef": altitudeRef}

        return gpsCoor
    else: return None

# End Extract Location=========================================
# convert GPSCoordinates to Degrees
# Input gpsCoordinates value from in EXIF Format
#
def ConvertAltToDegrees(gpsAltCoordinate):    
     if (gpsAltCoordinate != ''):
        n0 = gpsAltCoordinate[0]                                 
        n1 = gpsAltCoordinate[1]
        try:
            degreesAlt = float(n0) / float(n1)
        except:
            degreesAlt = 0.0
        floatCoordinate = float(degreesAlt)
        return floatCoordinate
     else:
        return 0.0
def ConvertToDegrees(gpsCoordinate):

    d0 = gpsCoordinate[0][0]
    d1 = gpsCoordinate[0][1]
    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0
    
    m0 = gpsCoordinate[1][0]
    m1 = gpsCoordinate[1][1]
    try:
        minutes = float(m0) / float(m1)
    except:
        minutes = 0.0

    s0 = gpsCoordinate[2][0]
    s1 = gpsCoordinate[2][1]
    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    floatCoordinate = float (degrees + (minutes / 60.0) + (seconds / 3600.0))
    return floatCoordinate 

    
