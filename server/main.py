# -*- coding: utf-8 -*-
from Mqtt     import Mqtt
from Songs    import Songs
from Podcasts import Podcasts
import mpd
import time

#http://pythonhosted.org/python-mpd2/topics/commands.html

ServerName   = 'hal'

if __name__ == '__main__':

    mpdServer = mpd.MPDClient()
    mpdServer.connect(ServerName, 6600)
    mpdServer.ping()

    print mpdServer.mpd_version

    # Load all Podcasts for test
    podcasts = Podcasts()

    # hack to set all active for now
    for i in podcasts.getNames():
        podcasts.setActive(i, True)

    podUrls  = podcasts.getUrls()

    # Load all Songs
    songs = Songs(mpdServer)

    # Empty current playlist
    mpdServer.clear()

    index = 0

    for i in songs.getSongs():

        mpdServer.add(i.getURI())

        # start after first song
        if index == 0:
            mpdServer.play()

        index += 1

        # add after every second song a podcast
        if index % 2 == 0 and len(podUrls) > 0:
            mpdServer.add(podUrls.pop())

        # give the mpd server some time to gigest
        time.sleep(2)

    # start the mqtt connection
    m = Mqtt(mpdServer, songs)
    m.start()

    mpdServer.close()
    mpdServer.disconnect()