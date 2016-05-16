#!/usr/bin/python
import requests
import bs4
import logging

'''
INPUT: string to search on imdb.com
OUTPUT: BeautifulSoup object containing html of the search return
'''
def imdbGetHtml(searchString):
    searchString = searchString.lower()
    searchString.replace(' ', '+')
    r = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + searchString + '&s=all')
    return bs4.BeautifulSoup(r.text, 'html.parser')


'''
INPUT: title string to search on imdb.com
OUTPUT: list of dictionaries of the following form scraped from imdb:
            title: title
            year: release year
            type: TV Show, Videogame, etc. Blank for films
            link: URL to imdb page
'''
def imdbTitleSearch(title):
    #get the BeautifulSoup4 for the title
    bSoup = imdbGetHtml(title)
    results = []
    #different modes to collect title, year, and type of result
    #from one search result
    modes = ['title', 'year', 'type']
    resultTable = bSoup.find('table', {'class': 'findList'})
    for td in resultTable.find_all('td', {'class': 'result_text'}):
        titleString = td.get_text().strip()
        info = {}
        #title, year, type
        for m in modes:
            info[m] = ''

        #assumes each result is of the form
        #title (year) (type, if not a movie)
        modeIndex = 0
        for ch in titleString:
            #if we find '(' strip the whitespace and move to the next mode
            if ch == '(':
                info[modes[modeIndex]] = info[modes[modeIndex]].strip()
                modeIndex += 1
                continue
            #if we find ')' and this is the last mode, then quit, else continue
            elif ch == ')':
                if modeIndex == len(modes) - 1:
                    break
                continue
            #otherwise add this character to the current mode
            info[modes[modeIndex]] += ch

        #if we saved a number as the year, make it an int, else make it None
        if info['year'].isdigit():
            info['year'] = int(info['year'])
        else:
            #if we don't get a year back, something strange happened and we
            #should record it
            sys.stderr.write("Issue with result from imdb recorded in log file\n")
            logging.warning("Issue in imdbTitleSearch with parsing the year")
            logging.warning("title input to function was %s",title)
            logging.warning("parsing title from imdb was %s",titleString)
            info['year'] = None
        info['link'] = 'http://www.imdb.com' + td.a.get('href')
        #creates a Media object and adds it to the results list
        results.append(info)
    return results

'''
INPUT: URL of a movie on imdb.com
OUTPUT: list of 2-tuples (name of actor, URL to actor's imdb page)
'''
def imdbGetActors(titleUrl):
    #get the BeautifulSoup4
    r = requests.get(titleUrl)
    bSoup = bs4.BeautifulSoup(r.text, 'html.parser')
    castList = bSoup.find('table', {'class': 'cast_list'})
    results = []
    for row in castList.find_all('td', {'itemprop': 'actor'}):
        name = row.find('span', {'itemprop': 'name'}).string
        link = row.a.get('href')
        results.append((name, link))
    return results

if __name__ == '__main__':
    getMovieActors('Watchmen', 2009)
