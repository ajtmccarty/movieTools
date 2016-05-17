# -*- coding: utf-8 -*-

import curses
import logging
import sys

'''
class to display a simple graphical interface through the command terminal to
make selections and return which item was selected
'''
class Selector:
    '''
    optionally can be initialized with the title and list of options to display
    otherwise, they can be given when printing the title or options
    '''
    def __init__(self,title="",options=[]):
        logging.info("selector.py: initializing window")
        #title for window
        self.title = title
        #options from which selection is made
        self.setOptions(options)
        #current selection
        self.selection = 0
        #list of items to print on bottom of screen as legend
        self.legend = []
        #initialize the curses window
        self.theWindow = curses.initscr()
        (self.height,self.width) = self.theWindow.getmaxyx()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.theWindow.keypad(1)

    '''
    must be called before closing to return the terminal to normal function
    '''
    def close(self):
        #clean up and exit
        curses.nocbreak()
        self.theWindow.keypad(0)
        curses.echo()
        curses.endwin()

    '''
    make sure options is a list of more than 1 item
    if not, log errors and quit
    '''
    def setOptions(self,options):
        if type(options) != type([]):
            self.close()
            sys.stderr.write("selector.py: options sent to selector are not a list, see log for more\n")
            logging.error("selector.py: options input to selector must be a list")
            logging.error("options input is "+ str(options) +" of type "+str(type(options)))
            sys.exit(0)
        if len(options) < 2:
            self.close()
            sys.stderr.write("selector.py: options must contain more than one option, see log for more\n")
            logging.error("selector.py: options input to selector must be a list of length greater than 1")
            logging.error("options input is "+ str(options) +" of length "+str(len(options)))
            sys.exit(0)
        #if these checks pass, we should be able to handle the options
        self.options = options

    '''
    refreshes the window, used when the display should be updated
    '''
    def refresh(self):
        self.theWindow.refresh()

    '''
    returns user input
    '''
    def getInput(self):
        return self.theWindow.getch()

    '''
    moves the highlighted field up one, unless it is at the top
    '''
    def moveCursorUp(self):
        #if we're at the top, do nothing
        if self.selection == 0:
            return
        #reprint the current selection without highlighting
        self.printOneOption(self.selection,self.options[self.selection])
        #update selection
        self.selection -= 1
        #print new selection with highlighting
        self.printOneOption(self.selection,self.options[self.selection],True)

    '''
    moves the highlighted field down one, unless at the bottom
    '''
    def moveCursorDown(self):
        #if we're at the bottom, do nothing
        if self.selection == (len(self.options) - 1):
            return
        #reprint the current selection without highlighting
        self.printOneOption(self.selection,self.options[self.selection])
        #update selection
        self.selection += 1
        #print new selection with highlighting
        self.printOneOption(self.selection,self.options[self.selection],True)

    '''
    turns on a one-field wide border around the entire window
    '''
    def setBorder(self):
        self.theWindow.box()
        return

    '''
    INPUT: y value, x value, text, highlighting
    OUTPUT: prints the text if it's valid
    if the string would be written off of the window, quits with an error and
    logs it
    '''
    def printText(self,y,x,text,highlight=False):
        #make sure the text is a string
        text = str(text)
        #check that it will be printed in the window
        if y < (self.height - 1) and (x+len(text) < (self.width - 1)):
            if highlight:
                self.theWindow.attrset(curses.A_REVERSE)
            else:
                self.theWindow.attrset(0)
            self.theWindow.addstr(y,x,text)
        else:
            sys.stderr.write("Tried to write outside the window\n")
            sys.stderr.write("max x: {} max y: {} write x: {} write y: {} \
                stringlength: {} \n".format(self.width,self.height,x,y,len(text)))
            self.close()
            sys.exit(0)

    '''
    INPUT: list of 2-tuples to print
                leg[0] is the key
                leg[1] is what the key does
    OUTPUT: prints the legend at the bottom of the screen
            if the format isn't valid, then log some errors
    '''
    def printLegend(self,legend=[]):
        if legend:
            #expect legend to be a list of tuples with the KEY followed by the
            #description
            for leg in legend:
                if (type(leg) != type((1,2))) or (len(leg) != 2):
                    sys.stderr.write("Issue with legend in selector, see log for more\n")
                    logging.warning("selector.py: bad legend input")
                    logging.warning("every legend entry should by a 2-tuple")
                    logging.warning("this entry is "+str(leg))
                #only add the valid entries to the legend
                else:
                    self.legend.append(leg)
        #print a horizontal line above the legend
        self.theWindow.hline(self.height-3,1,curses.ACS_HLINE,self.width-2)
        xPos = 2
        #second to last line
        yPos = self.height - 2
        legSep = "     "
        #print each legend entry one at a time and track the position of the cursor
        for i in range(len(self.legend)):
            leg = self.legend[i]
            #print the key highlighted
            self.printText(yPos,xPos,leg[0],True)
            xPos += len(leg[0])
            #separate the key and the description
            self.printText(yPos,xPos," - ",False)
            xPos += 3
            #print the description
            self.printText(yPos,xPos,leg[1],False)
            xPos += len(leg[1])
            #if it's not the last item, print the separator
            if i < (len(self.legend)-1):
                self.printText(yPos,xPos,legSep,False)
                xPos += len(legSep)
        return

    '''
    print the title at the top of the screen with a horizontal line under
    '''
    def printTitle(self,title=""):
        #make sure the title is a string
        title = str(title)
        #store the title if it's a new one
        if title:
            self.title = title
        #calculate number of spaces required to center the title
        spacesToCenter = (self.width - 2 - len(self.title))/2
        #print the title with the spaces on either side
        self.printText(1,1,(" "*spacesToCenter)+self.title)
        #horizontal line under title
        self.theWindow.hline(2,1,curses.ACS_HLINE,self.width-2)
        return

    '''
    INPUT: the index of the option, the option text, whether to highlight
    OUTPUT: prints the option
    '''
    def printOneOption(self,index,opt,highlight=False):
        #make the identifier string, deal with 0-indexing
        identifier = "(" + (str(index+1)) + ")"
        #print the number field as highlighted
        self.printText(index+3,2,identifier,highlight)
        #add a space and print the option text
        self.printText(index+3,2+len(identifier)," "+opt,False)

    '''
    INPUT: list of options, which to start with, both optional
    OUTPUT: prints the options
    '''
    def printOptions(self,options=[],startSelect=0):
        #if setting new options, make sure the option list is valid
        if options:
            self.setOptions(options)
        #go through the options
        for i in range(len(self.options)):
            #print each option, set highlighting true for the startSelect item
            self.printOneOption(i,self.options[i],i == startSelect)

if __name__ == "__main__":
    logging.basicConfig(filename='PyMovies.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
    logging.info("running selector from command line")
    theSel = Selector("The Window",["Thing1","Thing2","Thing3"])
    logging.info("window initialized")
    theSel.setBorder()
    logging.info("printing the title")
    theSel.printTitle()
    logging.info("title printed, moving on to options")
    theSel.printOptions()
    logging.info("options printed, moving on to legend")
    theSel.printLegend([("Up/Down","Navigate"),("S","Skip"),("Q","Quit")])
    logging.info("legend printed, waiting for input")
    x = ""
    while x != ord("q"):
        x = theSel.getInput()
        if x == 258:
            theSel.moveCursorDown()
        if x == 259:
            theSel.moveCursorUp()
        theSel.refresh()
    theSel.close()
    print "here"
