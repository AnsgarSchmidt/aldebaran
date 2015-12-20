# -*- coding: utf-8 -*-
import socket
import feedparser
import random

ALL = 0
TOP = 1
END = 2

podcastLinks = [
                [ 10, TOP, 'http://www.deutschlandfunk.de/podcast-forschung-aktuell.677.de.podcast.xml'],
                [ 10, TOP, 'http://www.deutschlandfunk.de/podcast-buechermarkt.701.de.podcast.xml'],
                [ 10, TOP, 'http://www.deutschlandfunk.de/podcast-campus-karriere.681.de.podcast.xml'],
                [ 10, TOP, 'http://www.deutschlandfunk.de/podcast-computer-und-kommunikation.685.de.podcast.xml'],
                [ 10, TOP, 'http://www.deutschlandfunk.de/podcast-informationen-am-abend.791.de.podcast.xml'],
                [ 10, END, 'http://www.fritz.de/media/podcasts/serien/fritzfressefreiheit.feed.podcast.xml'],
                [999, TOP, 'http://www.fritz.de/media/podcasts/serien/neues_vom_kaenguru_podcast.feed.podcast.xml'],
                [ 10, TOP, 'http://www.fritz.de/media/podcasts/fritzinfo/multimedia_und_games.feed.podcast.xml'],
                [ 10, TOP, 'http://www.fritz.de/media/podcasts/fritzinfo/buecher.feed.podcast.xml'],
                [ 10, TOP, 'http://www.fritz.de/media/podcasts/fritzinfo/neues-aus-der-netzwelt.feed.podcast.xml'],
                [ 10, TOP, 'http://www.fritz.de/media/podcasts/fritzinfo/film.feed.podcast.xml'],
                [ 10, TOP, 'http://www.fritz.de/media/podcasts/fritzinfo/platten.feed.podcast.xml'],
                [ 10, TOP, 'http://www1.wdr.de/radio/podcasts/wdr5/satirischewochenrueckblick100.podcast'],
                [  0, TOP, 'http://www1.wdr.de/radio/podcasts/wdr5/dasphilosophischeradio100.podcast'],
                [ 10, TOP, 'http://downloads.bbc.co.uk/podcasts/radio/stargazing/rss.xml'],
                [999, TOP, 'http://downloads.bbc.co.uk/podcasts/radio4/myshakespeare/rss.xml'],
                [999, TOP, 'http://downloads.bbc.co.uk/podcasts/worldservice/6min_vocab/rss.xml'],
                [999, TOP, 'http://downloads.bbc.co.uk/podcasts/worldservice/6min_gram/rss.xml'],
                [ 10, TOP, 'http://downloads.bbc.co.uk/podcasts/worldservice/tae/rss.xml'],
                [999, TOP, 'http://downloads.bbc.co.uk/podcasts/worldservice/how2/rss.xml'],
                [999, TOP, 'http://downloads.bbc.co.uk/podcasts/worldservice/elt_drama/rss.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndr2/programm/podcast2966.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndr2/programm/podcast2968.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndr2/fruehstueck_bei_stefanie/podcast2956.xml'],
                [ 10, TOP, 'http://www.n-joy.de/podcast/podcast4169.xml'],
                [ 10, TOP, 'http://www.n-joy.de/podcast/podcast4167.xml'],
                [ 10, TOP, 'http://www.ndr.de/info/podcast3002.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndrkultur/rezensionen/podcast3028.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndrkultur/rezensionen/podcast3036.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndrkultur/rezensionen/podcast3024.xml'],
                [ 10, TOP, 'http://www.ndr.de/ndrkultur/rezensionen/podcast3022.xml'],
                [ 10, TOP, 'http://www.ndr.de/radiomv/podcast3080.xml'],
                [ 10, TOP, 'http://www1.swr.de/podcast/xml/swr1/bw/swr1-durchgeschroedert.xml'],
                [ 10, TOP, 'http://www1.swr.de/podcast/xml/swr2/99sekunden.xml'],
                [ 10, TOP, 'http://www1.swr.de/podcast/xml/swr2/buch-der-woche.xml'],
                [ 10, TOP, 'http://www.inforadio.de/podcast/feeds/wissenswerte/wissenswerte.xml/feed=podcast.xml'],
                [ 10, TOP, 'http://www1.wdr.de/radio/podcasts/fhe/alltagosman102.podcast'],
                [ 10, TOP, 'http://www.ndr.de/podcast/podcast2956.xml'],
                [ 10, TOP, 'http://arvid9.hipcast.com/rss/braincast.xml'],
                [ 10, TOP, 'http://www.fraunhofer.de/de/rss/podcast.rss'],
                [999, TOP, 'http://www1.swr.de/podcast/xml/swr1/rp/stenkelfeld.xml'],
                [ 10, TOP, 'http://www1.wdr.de/radio/podcasts/wdr2/kino190.podcast'],
                [  0, TOP, 'http://www.davidbarrkirtley.com/podcast/geeksguideshow.xml'],
                [  0, TOP, 'http://www.howstuffworks.com/podcasts/stuff-you-should-know.rss'],
                [ 10, TOP, 'http://rss.sciam.com/sciam/60secsciencepodcast?format=xml']
               ]

class Podcast:

    def __init__(self, maxEpisodes, part, url):
        if url == None or len(url) == 0:
            raise Exception('No valid URL')
        self._url         = url
        self._maxEpisodes = maxEpisodes
        self._part        = part
        self._name        = 'NOT_SET'
        self._links       = []
        self._active      = False
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
        try:
            allLinks       = []
            self._links = []
            self._name  = 'NOT_SET'
            fp = feedparser.parse(self._url)
            if 'title' in fp['feed']:
                self._name = fp['feed']['title']
            else:
                print "No title: %s" % self._url
                self._name = self._url
            for entries in fp['entries']:
                if 'links' in entries:
                    for links in entries['links']:
                        if links['rel'] == 'enclosure':
                            allLinks.append(links['href'])
            if self._part == TOP:
                counter = 0
                for l in allLinks:
                    if counter < self._maxEpisodes:
                        self._links.append(l)
                        counter += 1
            if self._part == END:
                counter = len(allLinks)
                for l in allLinks:
                    if counter < self._maxEpisodes:
                        self._links.append(l)
                    counter -= 1
            if self._part == ALL:
                random.shuffle(allLinks)
                counter = 0
                for l in allLinks:
                    if counter < self._maxEpisodes:
                        self._links.append(l)
                        counter += 1
            print "%d of %d episodes at %s"%(len(self._links), len(allLinks), self._name)
        except Exception as e:
            print "Error in parsing feed:%s" % self._url
            print e

class Podcasts:

    def __init__(self):
        self._podcasts = {}
        for maxEpisodes, part, podcastLink in podcastLinks:
            p = Podcast(maxEpisodes, part, podcastLink)
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
    test.setActive(test.getNames()[0], True)
    print len(test.getUrls())