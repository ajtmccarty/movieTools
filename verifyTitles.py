#!/usr/bin/python

import os
import re
import PyMovies

TITLE_FILE = "./AllMovies.txt"

def checkTitles(tFile):
    with open(tFile,"r") as f:
        for movie in f:
            leftPar = movie.rfind("(")
            rightPar = movie.rfind(")")
            if (leftPar > 0) and (rightPar > 0):
                title = movie[:leftPar].strip()
                year = movie[leftPar+1:rightPar]
            elif (leftPar > 0) or (rightPar > 0):
                print "POTENTIAL ODD TITLE WARNING:"
                print movie
            else:
                year = ""
                period = movie.rfind(".")
                if period > 0:
                    title = movie[:period]
                else:
                    title = movie
            print title+"|"+year


if __name__ == "__main__":
    checkTitles(TITLE_FILE)
