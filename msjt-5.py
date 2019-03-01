#!/usr/bin/python
"""

 GlassBox Raspberry PI/Python Project to send morse code signal from 
 the top of St James' Chruch tower.

 Version V4

 2017 October 20

"""

    
# Import modules
import time
import signal
import RPi.GPIO as GPIO

import GlassBoxPythonLib as GBPL

def signal_handler(signal, frame):
    global interrupted
    interrupted = True
    
def ARBar():
# AR dit-dah-dit-dah-dit
    GBPL.outputDit ( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDash( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDit ( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDash( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDit ( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    
def CTBar():
# CT  dah-dit-dah-dit-dah
    GBPL.outputDash( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDit ( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDash( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDit ( GBPL.PIN, GBPL.DITTIMEINSECONDS )
    GBPL.outputDash( GBPL.PIN, GBPL.DITTIMEINSECONDS )
 
# Morse signal set up parameters
pin = 17
DitLength = 0.15

# Repeat the message every 120s
totaltime = 120

# Message 
# VVV
# Message components
VVV = "VVV"
Ca  = "SJC-TAUNTON.WEEBLY.COM"
str1 = " " +Ca +" "
message = VVV + str1

# Setup for stopping program gracefully with CTRL C
interrupted = False
signal.signal(signal.SIGINT, signal_handler)

# initialise GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,  GPIO.OUT)

# Setup Morse parameters
GBPL.SetupMorse( pin, DitLength )

# GBPL.PrintMe( message );                   # Print the message once

i=0                                        # A counter, set to zero
try:
    while True:
        time0 = time.time()                    # time "now" in seconds 
        i+= 1                                  # increment a counter
        CTBar();
        GBPL.MorseMe( message );               # Send the message
        ARBar();
        t = totaltime - (time.time() - time0)  # time = totatl time - (time now - time start)
        if t < 0:                              # If t is negative, set t=0
            t=0;
#      print(i,t)                            # Left here incase we need to know t
        time.sleep(t)
except (KeyboardInterrupt):
    GPIO.cleanup()                    # Clean up 
finally:
    print("Finished OK with ",i," repetitions")
# # # # # # # # # # # # #  THE END  # # # # # # # # # # # # #
