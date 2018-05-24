		*********Project 3: GPSExtraction README***********
			    Author: Michael Pedzimaz
	 
This Python project uses the PIL library to extract EXIF data (Exchangeable Image File
Format) from image files and break apart the various pieces of the meta data into a 
neatly formatted csv file that can be viewed in software such as Excel. This program was written 
in IDLE software using Python version 2.7.

It is composed of multiple required modules which are listed below:
GPSExtraction.py   --the main driver program that utilizes the various other modules for proper function
_modExif.py        --this module implements the PIL library and performs all PIL related tasks
_commandParser.py  --this is the location of the command line interface utility used within this Python software
_csvHandler.py     --this is our module for handling the output of our EXIF data dig into a neatly formatted csv file
classLogging	   --this module contains our _ForensicLog class that will be utilized for logging various program activities

We will need to specify three required command line arguments in order for this program to 
work:
-d  --our scanpath, which will contain images that will be scanned for EXIF data to retrieve
-c  --our destination location for the result csv file to be printed
-l  --our destination location for the log.txt to be printed 

To run this program using the Windows commmand prompt, the inputted string should look similar to:

>>> Python GPSExtraction.py -d C:\\images\ -c C:\\results\ -l C:\\log\

There is also a standalone Python file called "maliciousScript.py" which performs the task
of falisfying EXIF GPS information data within an image file. This includes producing 
randomly generated coordinates for latitude and longitude, as well as randomly generated
time of production. As the author of this script, I have to admit that I did not leave enough
time to get this standalone program working, which is why the file is loaded with comments 
regarding the procedure rather than the actual essence of a running program. However, I do 
thoroughly understand the processes that make up the workings of such a program and will
attempt to finish it past the due date and hopefully be able to turn it in for a few extra credit
points. 
Thank you for reading!
