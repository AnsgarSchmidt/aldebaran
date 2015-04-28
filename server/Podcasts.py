import socket
import feedparser
import random

podcastLinks = ['http://www.deutschlandfunk.de/podcast-forschung-aktuell.677.de.podcast.xml',
                'http://www.deutschlandfunk.de/podcast-buechermarkt.701.de.podcast.xml',
                'http://www.deutschlandfunk.de/podcast-campus-karriere.681.de.podcast.xml',
                'http://www.deutschlandfunk.de/podcast-computer-und-kommunikation.685.de.podcast.xml',
                'http://www.deutschlandfunk.de/podcast-informationen-am-abend.791.de.podcast.xml',
                'http://www.fritz.de/media/podcasts/serien/fritzfressefreiheit.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/serien/neues_vom_kaenguru_podcast.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/fritzinfo/multimedia_und_games.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/fritzinfo/buecher.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/fritzinfo/neues-aus-der-netzwelt.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/fritzinfo/film.feed.podcast.xml',
                'http://www.fritz.de/media/podcasts/fritzinfo/platten.feed.podcast.xml',
                'http://www1.wdr.de/radio/podcasts/wdr5/satirischewochenrueckblick100.podcast',
                # TO LONG 'http://www1.wdr.de/radio/podcasts/wdr5/dasphilosophischeradio100.podcast',
                'http://downloads.bbc.co.uk/podcasts/radio/stargazing/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/radio4/myshakespeare/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/worldservice/6min_vocab/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/worldservice/6min_gram/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/worldservice/tae/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/worldservice/how2/rss.xml',
                'http://downloads.bbc.co.uk/podcasts/worldservice/elt_drama/rss.xml',
                'http://www.ndr.de/ndr2/programm/podcast2966.xml',
                'http://www.ndr.de/ndr2/programm/podcast2968.xml',
                'http://www.ndr.de/ndr2/fruehstueck_bei_stefanie/podcast2956.xml',
                'http://www.n-joy.de/podcast/podcast4169.xml',
                'http://www.n-joy.de/podcast/podcast4167.xml',
                'http://www.ndr.de/info/podcast3002.xml',
                'http://www.ndr.de/ndrkultur/rezensionen/podcast3028.xml',
                'http://www.ndr.de/ndrkultur/rezensionen/podcast3036.xml',
                'http://www.ndr.de/ndrkultur/rezensionen/podcast3024.xml',
                'http://www.ndr.de/ndrkultur/rezensionen/podcast3022.xml',
                'http://www.ndr.de/radiomv/podcast3080.xml',
                'http://www1.swr.de/podcast/xml/swr1/bw/swr1-durchgeschroedert.xml',
                'http://www1.swr.de/podcast/xml/swr2/99sekunden.xml',
                'http://www1.swr.de/podcast/xml/swr2/buch-der-woche.xml',
                'http://www.inforadio.de/podcast/feeds/wissenswerte/wissenswerte.xml/feed=podcast.xml',
                'http://www1.wdr.de/radio/podcasts/fhe/alltagosman102.podcast',
                'http://www.ndr.de/podcast/podcast2956.xml',
                'http://arvid9.hipcast.com/rss/braincast.xml',
                'http://www.fraunhofer.de/de/rss/podcast.rss',
                'http://www1.swr.de/podcast/xml/swr1/rp/stenkelfeld.xml',
                'http://www1.wdr.de/radio/podcasts/wdr2/kino190.podcast',
                # To long 'http://www.davidbarrkirtley.com/podcast/geeksguideshow.xml',
                # To long 'http://www.howstuffworks.com/podcasts/stuff-you-should-know.rss',
                'http://rss.sciam.com/sciam/60secsciencepodcast?format=xml'
]

class Podcast:

    def __init__(self, url):
        if url == None or len(url) == 0:
            raise Exception('No valid URL')
        self._url    = url
        self._name   = 'NOT_SET'
        self._links  = []
        self._active = False
        socket.setdefaulttimeout(2)
        self.refresh()

    def getName(self):
        return self._name

    def getLinks(self):
        return self._links

    def isActive(self):
        return self._active

    def setActive(self, value):
        self._active = value

    def refresh(self):
        self._links = []
        self._name  = 'NOT_SET'
        fp = feedparser.parse(self._url)
        if 'title' in fp['feed']:
            self._name = fp['feed']['title']
        else:
            print "No title: %s" % self._url
            self._name = self._url
        for entries in fp['entries']:
            for links in entries['links']:
                if links['rel'] == 'enclosure':
                    self._links.append(links['href'])
        print "%d episodes at %s"%(len(self._links), self._name)

class Podcasts:

    def __init__(self):
        self._podcasts = {}
        for podcastLink in podcastLinks:
            p = Podcast(podcastLink)
            self._podcasts[p.getName()] = p

    def setActive(self, key, value):
        self._podcasts[key].setActive(value)

    def getNames(self):
        return self._podcasts.keys()

    def getUrls(self):
        urls = []
        for k,v in self._podcasts.items():
            if v.isActive():
                urls.extend(v.getLinks())
        random.shuffle(urls)
        return urls

    def refresh(self):
        for k,v in self._podcasts.items():
            v.refresh()

if __name__ == '__main__':

    test = Podcasts()

    print test.getNames()
    print len(test.getUrls())
    test.setActive(test.getNames()[0],True)
    print len(test.getUrls())