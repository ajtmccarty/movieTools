#!/usr/bin/python
import requests
import bs4

def imdbGetHtml(searchString):
    searchString = searchString.lower()
    searchString.replace(' ', '+')
    r = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + searchString + '&s=all')
    return bs4.BeautifulSoup(r.text, 'html.parser')


'''
return a list of Movie Objects for the specified input title
'''
def imdbTitleSearch(title):
    bSoup = imdbGetHtml(title)
    results = []
    modes = ['title', 'year', 'type']
    resultTable = bSoup.find('table', {'class': 'findList'})
    for td in resultTable.find_all('td', {'class': 'result_text'}):
        titleString = td.get_text().strip()
        info = {}
        for m in modes:
            info[m] = ''

        modeIndex = 0
        for ch in titleString:
            if ch == '(':
                info[modes[modeIndex]] = info[modes[modeIndex]].strip()
                modeIndex += 1
                continue
            elif ch == ')':
                if modeIndex == len(modes) - 1:
                    break
                continue
            info[modes[modeIndex]] += ch

        if info['year'].isdigit():
            info['year'] = int(info['year'])
        else:
            info['year'] = None
        print info
        link = 'http://www.imdb.com' + td.a.get('href')
        results.append(Media(info['title'],info['year'],info['type'],link))

    return results


def imdbGetActors(titleUrl):
    r = requests.get(titleUrl)
    bSoup = bs4.BeautifulSoup(r.text, 'html.parser')
    castList = bSoup.find('table', {'class': 'cast_list'})
    results = []
    for row in castList.find_all('td', {'itemprop': 'actor'}):
        name = row.find('span', {'itemprop': 'name'}).string
        link = row.a.get('href')
        results.append((name, link))

    return results


def titleSelector(searchTerm, options):
    print 'SEARCH TERM: ' + searchTerm
    print '---POTENTIAL MATCHES---'
    for tup in enumerate(options, 1):
        print '(' + str(tup[0]) + ') ' + tup[1]

    print '(N) No Good Match'
    isValid = False
    while not isValid:
        selection = raw_input('Please select best match or (N) for none:').lower()
        if selection != 'n' and not selection.isdigit():
            print 'Input must be a number or (N)'
            continue
        if selection == 'n':
            return None
        selection = int(selection)
        if selection < 1 or selection > len(options):
            print 'Input must be between 1 and ' + str(len(options))
            continue
        isValid = True

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
