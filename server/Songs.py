__author__ = 'ansi'

import random
import pickle
import ConfigParser
import mpd
import os
import sys

configFileName  = os.path.expanduser("~/.aldebaran.ini")
userMoods       = ['blacklist', 'sad', 'happy', 'lonely', 'morning', 'evening', 'sport']
dbDir           = '/Users/ansi/PycharmProjects/RadioTiffy/DB'

class Songs:

    def __init__(self, mpdServer):
        self._config     = ConfigParser.ConfigParser()
        self._readConfig()
        self._users      = {}
        self._mpdServer  = mpdServer
        self._percentage = 20
        for i in self._config.get('Songs','userNames').split(','):
            self._users[i] = User(i)

    def _readConfig(self):
        update = False
        if os.path.isfile(configFileName):
            print "Config file present"
            self._config.read(configFileName)
        else:
            print "Config file not present"
            update = True

        if not self._config.has_section('Songs'):
            print "Adding song part"
            update = True
            self._config.add_section('Songs')

        if not self._config.has_option('Songs', 'userNames'):
            print "No userNames Entry"
            update = True
            self._config.set('Songs','userNames', 'ansi,phawx,t1ntan')

        if update:
            with open(configFileName, 'w') as f:
                self._config.write(f)

    def getSongs(self):
        # Get all blacklists
        blacklist = []
        for user in self._users.itervalues():
            if user.isActive():
                for i in user.getBlacklistedSong():
                    blacklist.append(i.getKey())

        # Get all songs from users
        userSongs = []
        for user in self._users.itervalues():
            if user.isActive():
                for i in user.getSongs():
                    if i.getKey() not in blacklist:
                        userSongs.append(i)

        # Get new songs
        newSongs = []
        for pl in self._mpdServer.listplaylists():
            plName = pl['playlist']
            if plName.startswith('RandomSource|') or \
               plName.startswith('Starred')       or \
               plName.startswith('Eigene')        or \
               plName.startswith('User'):
                for song in self._mpdServer.listplaylistinfo(plName):
                    s = Song(song, True)
                    if s.isPlayable():
                        newSongs.append(s)

        #Load 10 songs at minimum in case there are not enough song in the playlists
        numNewSongs = max(100, int(len(userSongs) * (self._percentage / 100.0)))
        numNewSongs = min(numNewSongs, len(newSongs))

        random.shuffle(newSongs)
        for i in range(numNewSongs):
            userSongs.append(newSongs.pop())
        random.shuffle(userSongs)
        return userSongs

    def setPercentageNewSongs(self, percentage):
        self._percentage = percentage

    def addSongToMoodList(self, user, mood, data, mpd):
        #TODO remove it from all other lists
        self._users[user].addSongToMoodList(mood, data, mpd)

    def addSongToBlackList(self, user, data, mpd):
        addSongToMoodList(user, 'blacklist', data, mpd)

    def setMoodActive(self, user, mood, active):
        self._users[user].setMoodActive(mood, active)

    def setUserActive(self, user, active):
        self._active = active

    def getUsers(self):
        return userNames

class User:

    def __init__(self, name):
        self._name      = name
        self._active    = False
        self._playlists = {}

        if not os.path.isdir(dbDir):
            print "DB Dir not presents"
            os.mkdir(dbDir)

        fname = '%s/%s'%(dbDir,name)
        if not os.path.isdir(fname):
            print "User does not exists"
            os.mkdir(fname)

        for i in userMoods:
            fname = '%s/%s/%s.json'%(dbDir, name, i)
            self._playlists[i] = Playlist(i, name)
            self._playlists[i].setDBFileName(fname)

            if os.path.isfile(fname):
                self._playlists[i].load()
            else:
                print "DB does not exists"
                self._playlists[i].save()

    def setActive(self, value):
        self._active = value

    def isActive(self):
        return self._active

    def setMoodActive(self, mood, active):
        self._playlists[mood].setActive(active)

    def getSongs(self):
        songs = []
        for k, v in self._playlists:
            if v.isActive and not k == 'blacklist':
                songs.append(v.getSongs())

    def getBlacklistedSong(self):
        return self._playlists['blacklist']

    def addSongToMoodList(self, mood, data, mpd):
        self._playlists[mood].addSong(data, mpd)

class Playlist:

    def __init__(self, name, user):
        self._songs  = {}
        self._active = False
        self._name   = name
        self._user   = user

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def getSongs(self):
        return self._songs

    def setDBFileName(self, name):
        self._dbFileName = name

    def addSong(self, data, mpd):
        song = Song(data, mpd)
        song.addPlaylist(self._user, self._name)
        if song.isPlayable():
            self._songs[song.getKey()] = song
        self.save()

    def remove(self, key):
        self._songs.pop(key)

    def save(self):
        if self._dbFileName is not None and len(self._dbFileName) > 0:
            pickle.dump(self._songs, open(self._dbFileName, "wb"))

    def load(self):
        if self._dbFileName is not None and len(self._dbFileName) > 0:
            self._songs = pickle.load(open(self._dbFileName, "rb"))

    def __len__(self):
        return len(self.songs)

class Song:

    def __init__(self, data, mpd):
        if mpd:
            self._data = {}
            self._data['album']    =     data['album']
            self._data['title']    =     data['title']
            self._data['track']    = int(data['track'] )
            self._data['artist']   =     data['artist']
            self._data['file']     =     data['file']
            self._data['time']     = int(data['time']  )
            self._data['playlist'] = {}
        else:
            self._data  = data

    def addPlaylist(self, user, playlist):
        self._data['playlist'][user] = playlist

    def isPlayable(self):
         return self._data['time'] > 0

    def getKey(self):
        return self._data['file']

    def getURI(self):
        return self._data['file']

    def getTitle(self):
        return self._data['title']

    def getAlbum(self):
        return self._data['album']

    def getTrack(self):
        return self._data['track']

    def getArtist(self):
        return self._data['artist']

    def getTime(self):
        return self._data['time']

    def getDBEntry(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __eq__(self, other):
        if other is not None and \
        self._data['album']  == other._data['album']  and \
        self._data['title']  == other._data['title']  and \
        self._data['track']  == other._data['track']  and \
        self._data['artist'] == other._data['artist'] and \
        self._data['file']   == other._data['file']   and \
        self._data['time']   == other._data['time']:
            return True
        else:
            return False

if __name__ == "__main__":

    mpdServer = mpd.MPDClient()
    mpdServer.connect('badeserver', 6600)
    mpdServer.ping()
    print mpdServer.mpd_version

    songs = Songs(mpdServer)
    for i in songs.getSongs():
        print i

    mpdServer.close()
    mpdServer.disconnect()