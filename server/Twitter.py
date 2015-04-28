from twitter import *
import os
import requests
import ConfigParser

homeDir          = os.path.expanduser("~/.aldebaran")
configFileName   = homeDir + '/config.ini'
config           = ConfigParser.ConfigParser()

def readConfig():
    update = False

    if not os.path.isdir(homeDir):
        print "Creating homeDir"
        os.makedirs(homeDir)

    if os.path.isfile(configFileName):
        print "Config file present"
        config.read(configFileName)
    else:
        print "Config file not present"
        update = True

    if not config.has_section('Twitter'):
        print "Adding Twitter part"
        update = True
        config.add_section('Twitter')

    if not config.has_option('Twitter', 'consumerKey'):
        print "No consumerKey Entry"
        update = True
        config.set('Twitter','consumerKey', '<consumerKey>')

    if not config.has_option('Twitter', 'consumerSecret'):
        print "No consumerSecret Entry"
        update = True
        config.set('Twitter','consumerSecret', '<consumerSecret>')

    if not config.has_option('Twitter', 'AccessToken'):
        print "No AccessToken Entry"
        update = True
        config.set('Twitter','AccessToken', '<AccessToken>')

    if not config.has_option('Twitter', 'AccessSecret'):
        print "No AccessSecret Entry"
        update = True
        config.set('Twitter','AccessSecret', '<AccessSecret>')

    if not config.has_section('Watson'):
        print "Adding Watson part"
        update = True
        config.add_section('Watson')

    if not config.has_option('Watson', 'WatsonAuthKey'):
        print "No WatsonAuthKey Entry"
        update = True
        config.set('Watson','WatsonAuthKey', '<WatsonAuthKey>')

    if not config.has_option('Watson', 'WatsonAuthPass'):
        print "No WatsonAuthPass Entry"
        update = True
        config.set('Watson','WatsonAuthPass', '<WatsonAuthPass>')

    if update:
        with open(configFileName, 'w') as f:
            config.write(f)

def getOgg(text):

    res = requests.get("https://stream.watsonplatform.net/text-to-speech-beta/api/v1/synthesize",
                       auth=(config.get('Watson','WatsonAuthKey'), config.get('Watson','WatsonAuthPass')),
                       params={'text': text, 'voice': 'VoiceEnUsMichael', 'accept': 'audio/ogg; codecs=opus'},
                       stream=True,
                       verify=False
                      )
    return res.content

if __name__ == '__main__':

    print "Twitter"

    readConfig()

    t = Twitter(auth=OAuth(consumer_key    = config.get('Twitter' , 'consumerKey'),
                           consumer_secret = config.get('Twitter' , 'consumerSecret'),
                           token           = config.get('Twitter' , 'AccessToken'),
                           token_secret    = config.get('Twitter' , 'AccessSecret')
                          )
               )
    tweets =  t.statuses.home_timeline()

    index = 0
    for i in tweets:
        user = i['user']['screen_name']
        cont = i['text']
        text = 'Breaking news. The user %s just announced on twitter %s'%(user, cont)
        print text
        filename = 'test%i.ogg'%index
        with open("/tmp/"+filename, 'w') as f:
            f.write(getOgg(text))
        index += 1