#
# Python Ping Sweep GUI Application
#
# import the necessary modules
import wx          # Import the GUI module wx
import sys          # Import the standard library module sys
import pyping     # Import the ICMP Ping Module 
import socket     # Import the standard library module socket
import random
import time

from time import gmtime, strftime # import time functions

#
# Event Handler for the pingScan Button Press
# This is executed each time the Scan Button is pressed on the GUI
#

def pingScan(event):
    # Since the user specifies a range of Hosts to Scan, I need to verify
    # that the startHost value is <= endHost value before scanning
    # this would indicate a valid range
    # If not I need to communicate the error with the user
    if hostEnd.GetValue() < hostStart.GetValue():
        # This is an improper setting
        # Notify the user using a wx.MessageDialog Box
        dlg = wx.MessageDialog(mainWin, "Invalid Local Host Selection", "Confirm",
                               wx.OK | wx.ICON_EXCLAMATION)
        result = dlg. ShowModal()
        dlg.Destroy()
        return

    # If we have a valid range update the Status Bar
    mainWin.StatusBar.SetStatusText('Executing Ping Sweep . . . . Please Wait')

    # Record the Start Time and Update the results window

    utcStart = gmtime()
    utc = strftime("%a, %d %b %Y %X +0000", utcStart)
    results.AppendText("\n\nPing Sweep Started: " +utc+ "\n\n")

    # Similar to the example script at the beginning of the chapter
    # I need to build the base IP Address String
    # Extract data from the ip Range and host name user selections
    # BUild a Python LIst of IP Addresses to Sweep

    baseIP = str(ipaRange.GetValue())+'.'+str(ipbRange.GetValue())+'.'+str(ipcRange.GetValue())+'.'

    ipRange = []

    for i in range(hostStart.GetValue(), (hostEnd.GetValue()+1)):
        ipRange.append(baseIP+str(i))

    # For each of the IP Addresses in the ipRange List, Attempt a PING
    for ipAddress in ipRange:
        try:
            # Report the IP Address to the Window Status Bar
            # Prior to the attempt

            mainWin.StatusBar.SetStatusText('Pinging IP: '+ipAddress)
            # Perform the Ping
            if stealthMode.GetValue() == False:
                pingInfo = pyping.ping(ipAddress, timeout = 1000, count = 1)
            elif stealthMode.GetValue() == True:
                rndPingInt = random.randint(2,10)
                # print rndPingInt
                time.sleep(rndPingInt)
                pingInfo = pyping.ping(ipAddress, timeout = 1000, count = 1)
            
            #Display the IP Address in the Main Window
            results.AppendText(ipAddress+'\t')

            if pingInfo.ret_code == 0:
                # If Successful (i.e. no timeout) display
                # the result and response time

                results.AppendText('Response Success')
                results.AppendText('\t')
                results.AppendText(' Response Time: '+str(pingInfo.avg_rtt)+' Milliseconds')
                results.AppendText("\n")
            else:
                # If pingInfo == 1, then the request timed out
                # Report the Response Timeout
                results.AppendText('Response Timeout')
                results.AppendText("\n")

        except socket.error, e:
            # If any socket Errors occur Report the offending IP
            # along with any error information provided by the socket

            results.AppendText(ipAddress)
            results.AppendText('Response Failed: ')
            results.AppendText(e.message)
            results.AppendText("\n")
    # Once all ipAddresses are processed
    # Record and display the ending time of the sweep

    utcEnd = gmtime()
    utc = strftime("%a, %d %b %Y %X + 0000", utcEnd)
    results.AppendText("\nPing Sweep Ended: "+ utc + "\n\n")

    #Clear the Status Bar
    mainWin.StatusBar.SetStatusText('')

    return

# End Scan Event Handler ===============================

#
# Program Exit Event Handler
# This is executed when the user presses the exit button
# The program is terminated using the sys.exit() method
#

def programExit(event):
    sys.exit()

# End Program Exit Event Handler =========================

#
# Setup the Application Windows ==========================
#
# This section of code sets up the GUI environment
#

# Instantiate a wx.App() object
app = wx.App()

# define the main window including the size and title
mainWin = wx.Frame(None, title = "Simple Ping (ICMP) Sweeper 1.0", size = (1000,600))

# define the action panel, this is the area where the buttons and spinners are located
panelAction = wx.Panel(mainWin)
# define action buttons
# I'm creating two buttons, one for Scan and one for Exit
# Notice that each button contains the name of the function that will
# handle the button press event - - pingScan and ProgramExit respectively
stealthMode = wx.CheckBox(panelAction, -1, 'Stealth Mode', (10, 10))
stealthMode.SetValue(False)

scanButton = wx.Button(panelAction, label = 'Scan')
scanButton.Bind(wx.EVT_BUTTON, pingScan)

exitButton = wx.Button(panelAction, label = 'Exit')
exitButton.Bind(wx.EVT_BUTTON, programExit)

# define a Text Area where I can display results
results = wx.TextCtrl (panelAction, style = wx.TE_MULTILINE | wx.HSCROLL)

# Base Network for Class C IP Addresses have 3 components
# For class C addresses, the first 3 octets (24 bits) define the network
# e.g., 127.0.0
# the last octet (8 bits) defines the host i.e., 0 -255
# Thus I setup 3 spin controls one for each of the 3 network octets
# I also set the default value to 127.0.0 for convenience
ipaRange = wx.SpinCtrl(panelAction, -1, '')
ipaRange.SetRange(0,255)
ipaRange.SetValue(127)

ipbRange = wx.SpinCtrl(panelAction, -1, '')
ipbRange.SetRange(0,255)
ipbRange.SetValue(0)

ipcRange = wx.SpinCtrl(panelAction, -1, '')
ipcRange.SetRange(0,255)
ipcRange.SetValue(0)

# Also, I'm adding a label for the user
ipLabel = wx.StaticText(panelAction, label = "IP Base: ")

# Next, I want to provide the user with the ability to set the host range
# they wish to scan. Range is 0-255

hostStart = wx.SpinCtrl(panelAction, -1, '')
hostStart.SetRange(0,255)
hostStart.SetValue(1)

hostEnd = wx.SpinCtrl(panelAction, -1, '')
hostEnd.SetRange(0, 255)
hostEnd.SetValue(10)

HostStartLabel = wx.StaticText(panelAction, label = "Host Start: ")
HostEndLabel = wx.StaticText(panelAction, label = "Host End: ")

# Now I create BoxSizer to automatically align the different components
# neatly within the panel
# First I create a horizontal Box
# I'm adding the buttons, ip Range and Host Spin Controls

actionBox = wx.BoxSizer()

actionBox.Add(stealthMode, proportion = 0, flag=wx.LEFT|wx.CENTER, border = 5)
actionBox.Add(scanButton, proportion = 0, flag=wx.LEFT, border = 5 )
actionBox.Add(exitButton, proportion = 0, flag=wx.LEFT, border = 5 )

actionBox.Add(ipLabel, proportion = 0, flag = wx.LEFT, border = 5)

actionBox.Add(ipaRange, proportion = 0, flag=wx.LEFT, border = 5)
actionBox.Add(ipbRange, proportion = 0, flag=wx.LEFT, border = 5)
actionBox.Add(ipcRange, proportion = 0, flag=wx.LEFT, border = 5)

actionBox.Add(HostStartLabel, proportion = 0, flag = wx.LEFT|wx.CENTER,
              border = 5)
actionBox.Add(hostStart, proportion=0, flag = wx.LEFT, border = 5)

actionBox.Add(HostEndLabel, proportion = 0, flag= wx.LEFT|wx.CENTER, border = 5)
actionBox.Add(hostEnd, proportion = 0, flag = wx.LEFT, border = 5)

# Next I create a Vertical Box that I place the Horizontal Box Inside
# Along with the results text area

vertBox = wx.BoxSizer(wx.VERTICAL)
vertBox.Add(actionBox, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
vertBox.Add(results, proportion = 1, flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

# I'm adding a status bar to the main windows to display status messages

# Finally, I use the SetSizer function to automatically size the windows
# based on the definitions above

panelAction.SetSizer(vertBox)

# Display the main window
mainWin.CreateStatusBar()
mainWin.Show()

# Enter the Applications Main Loop
# Awaiting User Actions
app.MainLoop()

