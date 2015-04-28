import mpd
import json
import paho.mqtt.client as mqtt
import threading
from Songs import Songs
from Songs import Song

class Mqtt(threading.Thread):

    def __init__(self, mpd, songs):
        threading.Thread.__init__(self)
        self._mqclient = mqtt.Client("Aldebaran", clean_session=True)
        self._mpd = mpd
        self._song = songs
        self.setDaemon(True)

    def on_connect(self, client, userdata, rc, b):
        print("Connected with result code "+str(rc))
        client.subscribe("livingroom/radio/#")

    def on_message(self, client, userdata, msg):
        #print "Mq Received on channel %s -> %s" % (msg.topic, msg.payload)
        topics = msg.topic.split('/')
        if len(topics) == 6     and \
            topics[2] == 'song' and \
            topics[3] == 'add':
            user   = topics[4]
            mood   = topics[5]
            print msg.payload
            song   = json.loads(msg.payload)
            print user
            print mood
            print song

            self._song.addSongToMoodList(user, mood, song, False)

    def run(self):
        self._mqclient.connect("ansinas", 1883, 60)
        self._mqclient.on_connect = self.on_connect
        self._mqclient.on_message = self.on_message
        self._mqclient.loop_forever()

    def post(self, channel, msg):
        self._mqclient.publish(channel, msg)

    def stop(self):
        self._mqclient.loop_stop(True)

if __name__ == '__main__':
    print "MQTT"

    mpdServer = mpd.MPDClient()
    mpdServer.connect('ansinas', 6600)
    mpdServer.ping()

    songs = Songs(mpdServer)

    m = Mqtt(mpdServer, songs)
    m.start()

    currentSong = None

    while True:
        mpdServer.idle()
        cs = Song(mpdServer.currentsong(), True)
        if not cs == currentSong:
            m.post("livingroom/radio/current/song", str(cs))
            currentSong = cs
