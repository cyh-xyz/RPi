
"""

This file is GlassBoxPythonLib.py

A colelction of routines developed for various projects produced
by Taunton Library Glass Box Raspberry Pi Group

Libraries imported RPi.GPIO, time, numpy

Version v 1.3

2017 September 4

# # # # # # # # # #   THE FUNCTIONS  # # # # # # # # # # # # #

   The list of functions, in alphabetic order, are:

   Name                         Function
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
   char2morse( L ):             Character to morse code
   MorseandPrintMe( str ):      Print morse code then produce tones
   outputDash( pin, s):         Proudce Dash tone
   outputDit( pin, s ) :        Proudce Dit tone, s seconds long
   outputInterLetterGap( s ):   Inter-letter gap s seconds between tone
   outputInterWordGap( s ):     Inter-word gap s seconds between tone
   PrintMe( str ):              Print the string and its morse code
   MorsetMe( str ):             Produce morse tones of the string
   SetUpMorse ( pin, s )        Set global variables for pin no. & length of tone

# # # # # # # # # #   GLOBAL Variabes  # # # # # # # # # # # # #
   
   Name                         Function
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    PIN              -  the number of the pin to which the sound is being made
    DITTIMEINSECONDS -  the length of time, in secons, for a dit, e.g. 0.05
    HIGH             -  1 settings for GPIO
    LOW              -  0 settings for GPIO
"""

import numpy as np
import time
import RPi.GPIO as GPIO

def char2morse (L):

    """
    - - - - - - -
    char2morse
    - - - - - - -
 
    Given one character this routine checks that it is either an uppercase
    letter from A to Z, or a number (character) from 0 to 9, or one of the 
    special syymbos that incldue punctuation, and returns a list of  0's 
    and 1's giving the sequence of dits(0) and dahs(1) that make the 
    morse code character.  
    If -1 is returned, then the given character was out of the specified range.

    Arrays storage:
    malpha[0:25, 0:4] Code for morse code for each letter (capital) of the 
                    alphabet.  First index, number 0 to 25, with 0 for A, 
                    1 for B ..., and 25 for Z
                    Second index, numbers 0 to 5, the first element gives
                    the number of dits(0) and dahs(1) that define the letter
                    (-1 => not used).  Examples
                    A -> dit dah => malpha[0] = 2, 0, 1 
                    
    mnos[0:9, 0:5]  Code for morse code for numbers 0 to 9
    msym[0:11, 0:5] Punctuation and symbols
    """
    
#   Morse code definitions for A, B, C, ... Z
    malpha = np.array([
               [ 2,  0,  1, -1, -1 ],    # A => 0
               [ 4,  1,  0,  0,  0 ],    # B => 1
               [ 4,  1,  0,  1,  0 ],    # C => 2
               [ 3,  1,  0,  0, -1 ],    # D => 3
               [ 1,  0, -1, -1, -1 ],    # E => 4
               [ 4,  0,  0,  1,  0 ],    # F => 5
               [ 3,  1,  1,  0, -1 ],    # G => 6
               [ 4,  0,  0,  0,  0 ],    # H => 7
               [ 2,  0,  0, -1, -1 ],    # I => 8
               [ 4,  0,  1,  1,  1 ],    # J => 9
               [ 3,  1,  0,  1, -1 ],    # K => 10
               [ 4,  0,  1,  0,  0 ],    # L => 11
               [ 2,  1,  1, -1, -1 ],    # M => 12
               [ 2,  1,  0, -1, -1 ],    # N => 13
               [ 3,  1,  1,  1, -1 ],    # O => 14
               [ 4,  0,  1,  1,  0 ],    # P => 15
               [ 4,  1,  1,  0,  1 ],    # Q => 16
               [ 3,  0,  1,  0, -1 ],    # R => 17
               [ 3,  0,  0,  0, -1 ],    # S => 18
               [ 1,  1, -1, -1, -1 ],    # T => 19
               [ 3,  0,  0,  1, -1 ],    # U => 20
               [ 4,  0,  0,  0,  1 ],    # V => 21
               [ 3,  0,  1,  1, -1 ],    # W => 22
               [ 4,  1,  0,  0,  1 ],    # X => 23
               [ 4,  1,  0,  1,  1 ],    # Y => 24
               [ 4,  1,  1,  0,  0 ]]);  # Z => 25

#   Morse code definitions for numbers 0, 1, 2, ... 9
    mnos = np.array([
               [ 5, 1, 1, 1, 1 ,1 ],     # 0
               [ 5, 0, 1, 1, 1, 1 ],     # 1
               [ 5, 0, 0, 1, 1, 1 ],     # 2
               [ 5, 0, 0, 0, 1, 1 ],     # 3
               [ 5, 0, 0, 0, 0, 1 ],     # 4
               [ 5, 0, 0, 0, 0, 0 ],     # 5
               [ 5, 1, 0, 0, 0, 0 ],     # 6
               [ 5, 1, 1, 0, 0, 0 ],     # 7
               [ 5, 1, 1, 1, 0, 0 ],     # 8
               [ 5, 1, 1, 1, 1, 0 ]]);   # 9

# Punctation and other symbpls " ' ( ) , - . / : = ? @
    syms = ["", "'", "(", ")", ",", "-", ".", "/", ":", "=", "?", "@"]

# Morse Code for symbols
    msyms = np.array([
             [ 6,  0,  1,  0,  0,  1,  0 ],    # " Quotation
             [ 6,  0,  1,  1,  1,  1,  0 ],    # ' Apostrophe
             [ 5,  1,  0,  1,  1,  0, -1 ],    # ( Open paraenthesis
             [ 6,  1,  0,  1,  1,  0,  1 ],    # ) Close parenthesis
             [ 6,  1,  1,  0,  0,  1,  1 ],    # , Comma
             [ 6,  1,  0,  0,  0,  0,  1 ],    # - hyphen
             [ 6,  0,  1,  0,  1,  0,  1 ],    # . Period (full stop)
             [ 5,  1,  0,  0,  1,  0, -1 ],    # / Slash
             [ 6,  1,  1,  1,  0,  0,  0 ],    # : Colon
             [ 5,  1,  0,  0,  0,  1, -1 ],    # = Equals
             [ 6,  0,  0,  1,  1,  0,  0 ],    # ? Question mark
             [ 6,  0,  1,  1,  0,  1,  0 ]]);  # @ At sign

# Function ord gives the Unicorde value of the character
# in order to calculate the position of the character in the table
    na = ord("A");
    nz = ord("Z");
    n0 = ord("0");
    n9 = ord("9");

# Find if the character is a symbol and not an alphabetc character or a number
    sym = L in syms;

# Code for the given character
    nl = ord(L);

# Letter or number
    if nl >= na  and nl <= nz :      # Character is a Capital letter
       i = nl - na                   # Our index for the character
       m = malpha[i,0] + 1           # Pointer to end for extractting code
       b = malpha[i, 1:m]            # Extract morse code
    elif nl >= n0 and nl <= n9 :     # Number 0 to 9 
       i = nl - n0
       b = mnos[i, 1:6]
    elif sym :                       # One of the symbols
        i = syms.index(L)
        m = msyms[i,0] + 1
        b = msyms[i, 1:m]
#        print("\nsymbol index", i, syms[i], b)
    else:                            # Unrecognised
       b =[-1]

    return b;

# Print function

def MorseMe( str ):
    """
    This function takes each character of the string str and converts it
    to morse code.  The code is then submitted to routines that use the 
    GPIO to give the correct, tone.
    GPIO routines can produce the appropriate tone.
    Dit is given by 0
    Dah is given by 1
    """
    
    n = len(str);                         # Number of characters is the string
    for i in range(0,n,1):                # Loop for each character
        ch = str[i].upper();              # Only deal with uppere case characters
        if ch.isspace():                  # Character is a space
            outputInterWordGap( DITTIMEINSECONDS )
        else:                             # Convert character to morse 
            code = char2morse(ch);        # Get code for morse
            if code[0] >0 -1:             # Morse code for character, otherwise ignore 
                for i in range(0,len(code),1):      # Loop for each dit or dah
                    j = code[i]
                    if j == 0:
                        outputDit( PIN, DITTIMEINSECONDS )
                    else:
                        outputDash( PIN, DITTIMEINSECONDS )
                outputInterLetterGap( DITTIMEINSECONDS ) # Tone between letters
    return
    
def PrintMe( str ):
    """
    This function takes the string (str) and prints it to the screen, then
    converts each characters to morse code, both of which are also printed.  
    A message will be  printed if there is no morese translation.
    Dit is given by 0
    Dah is given by 1 - 3 times longer than dit
    """
    
    print(str);                           # Print the submitted string
    n = len(str);                         # Number of characters is the string
    for i in range(0,n,1):                # Loop for each character
        ch = str[i].upper();              # Only deal with uppere case characters
        if ch.isspace():                  # Character is a space
            print (" ")                   # Print code for the record
        else:                             # Convert character to morse 
            code = char2morse(ch);        # Get code for morse
            if code[0] == -1:             # No morse code for this character 
                print ("\n     Error: Unknown character '",ch, "' found in ",str," and was ignored.", sep="",end="")
            else:                         # Print morse code and submit to get tone
                print("\n"+ch, end=" => ")          # Print the character, no line feed advance
                for i in range(0,len(code),1):      # Loop for each dit or dah
                    j = code[i]
                    if j == 0:
                        print ("Dit", end=" ")      # Print code for the record
                    else:
                        print ("Dah", end=" ")      # Print code for the record
    print("\n")                                     # New line for the printed record
    return
    

def outputDash( pin, ditTimeInSeconds ):
    GPIO.output(pin, HIGH)
    time.sleep(ditTimeInSeconds*3.0)
    GPIO.output(pin, LOW)
    time.sleep(ditTimeInSeconds)
    return

def outputDit(pin, ditTimeInSeconds ):
    GPIO.output(pin, HIGH)
    time.sleep(ditTimeInSeconds)
    GPIO.output(pin, LOW)
    time.sleep(ditTimeInSeconds)
    return

def outputInterLetterGap( ditTimeInSeconds ):
    time.sleep(ditTimeInSeconds*3.0)
    return

def outputInterWordGap( ditTimeInSeconds ):
    time.sleep(ditTimeInSeconds*7.0)
    return

def MorseandPrintMe (str):
    PrintMe(str);
    print("Starting tones");
    MorseMe(str);
    print("End of tones\n");
    return
    
def SetupMorse ( i, s):
    """
    A routine to set the global variables for the pin number, the length of 
    a dit in seconds  as well as the level code.

    PIN              -  the number of the pin to which the sound is being 
                        made, e..g. 17
    DITTIMEINSECONDS -  the length of time, in secons, for a dit, 
                        e.g. 0.02
    
    HIGH             -  1 
    LOW              -  0
    
    PIN & DITTIMEINSECONDS are arguments of the call and thus may be changed
    
    Convention is that all global variables are given with uppercase letters.
    """

    global PIN, DITTIMEINSECONDS;
    global HIGH, LOW;
    PIN  = i;
    HIGH = 1;
    LOW  = 0;
    DITTIMEINSECONDS = s;
##!    print (PIN, DITTIMEINSECONDS)
    return

# # # # # # # # # #   END FUNCTIONS  # # # # # # # # # # # # #

