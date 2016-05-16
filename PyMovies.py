#!/usr/bin/python
import requests
import bs4

def search(title, year):
    results = []
    for i in range(len(searchDict['movies'])):
        thisMovie = searchDict['movies'][i]
        year = thisMovie['release-date'][:4]
        results.append((i, thisMovie['title'], year))

    return results


def allSearch(title, year):
    url = 'https://boxofficebuz.p.mashape.com/v1/movie/search/'
    headers = {'X-Mashape-Key': 'o2UzVbD7xMmshaVs2OmyxPeEbiCRp1V05ddjsnp1xUCip3E33e',
     'Accept': 'application/json'}
    r = requests.get(url + title, headers=headers)
    searchDict = r.json()
    return searchDict

'''
Utility for selecting an option from a list
INPUT: the search term and the list of possible options
OUTPUT: the index of the selected option or None
'''
def titleSelector(searchTerm, options):
    print 'SEARCH TERM: ' + searchTerm
    print '---POTENTIAL MATCHES---'
    #print out all the possible matches in options with an index
    for tup in enumerate(options, 1):
        print '(' + str(tup[0]) + ') ' + tup[1]
    #add an option for no good match
    print '(N) No Good Match'
    isValid = False
    #handle user input
    while not isValid:
        selection = raw_input('Please select best match or (N) for none:').lower()
        #must be 'n' or a number
        if selection != 'n' and not selection.isdigit():
            print 'Input must be a number or (N)'
            continue
        if selection == 'n':
            return None
        #if it's not 'n' here, then it must be a number
        selection = int(selection)
        #make sure it's an appropriate number
        if selection < 1 or selection > len(options):
            print 'Input must be between 1 and ' + str(len(options))
            continue
        isValid = True

    #subtract 1 b/c options start at 1 but list is 0 indexed
    return selection - 1

def getMovieActors(title, year):
    #get list of possible Movie Objects
    optionList = imdbTitleSearch(title)
    #find index of correct Movie object, if it exists
    index = titleSelector(title + ' - ' + str(year), [ m.getTitle() + ' - ' + str(m.getYear()) for m in optionList ])
    #get the actors of the Movie object
    actors = imdbGetActors(optionList[index].getLink())
    for actor in actors:
        print actor[0]


if __name__ == '__main__':
    getMovieActors('Watchmen', 2009)
