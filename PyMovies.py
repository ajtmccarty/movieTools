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


def imdbGetHtml(searchString):
    searchString = searchString.lower()
    searchString.replace(' ', '+')
    r = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + searchString + '&s=all')
    return bs4.BeautifulSoup(r.text, 'html.parser')


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
        link = 'http://www.imdb.com' + td.a.get('href')
        results.append((info['title'],
         info['year'],
         info['type'],
         link))

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
    optionList = imdbTitleSearch(title)
    index = titleSelector(title + ' - ' + str(year), [ x[0] + ' - ' + str(x[1]) for x in optionList ])
    actors = imdbGetActors(optionList[index][2])
    for actor in actors:
        print actor[0]


if __name__ == '__main__':
    x = allSearch('Watchmen', 2009)
    print 'WATCHMEN STARS:'
    print x['movies'][1]['starring']
