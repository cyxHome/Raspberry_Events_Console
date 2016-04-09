import urllib
from bs4 import *

def retieveEvents():
    # root website
    url = 'https://events.cornell.edu/'

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    briefs = soup.select("div.item.event_item.vevent")

    # retieve all the events detail pages url.
    print 'collecting', len(briefs), 'events from', url
    count = len(briefs)
    toVisit = []
    for brief in briefs:
        toVisit.append(brief.find('a').get('href'))

    result = []

    # get information from each events detail pages.
    for item in toVisit:
        tmp = {}
        url = item
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        event = soup.select("div.box_header.vevent")[0]

        title = event.h1.span.get_text().strip()
        time = event.h2.abbr.get_text().strip()
        location = event.h3.a
        if location is not None:
            location = location.get_text().strip()
        else:
            location = "Cornell University"
        street = event.h3.small
        if street is not None:
            street = street.get_text().strip()
        else:
            street = "Cornell University"
        description = event.select("div.description")
        if len(description) > 0:
            description = description[0].get_text()
        else:
            description = ""
        image = soup.select("div.box_image")
        if len(image) > 0:
            image = image[0].a.img['src']
        else:
            image = ""
        tmp['title'] = title
        tmp['time'] = time
        tmp['location'] = location
        tmp['description'] = description
        tmp['image'] = image
        print 'retrieved:', tmp['title']
        result.append(tmp)
        count = count - 1

    # return all events dicitionary in an array.
    return result

if __name__ == '__main__':
    print retieveEvents()
