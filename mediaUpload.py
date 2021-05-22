import os
from os import path
import sys
import time
import configparser
import magic
import json
import requests
from requests_oauthlib import OAuth1

#twitter endpoints
MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

#read config
creds = 'credConfig.cfg'
config = configparser.ConfigParser()
config.read(creds)
CONSUMER_KEY = config['twitter']['consumerKey']
CONSUMER_SECRET = config['twitter']['consumerSecret']
ACCESS_TOKEN = config['twitter']['accessToken']
ACCESS_TOKEN_SECRET = config['twitter']['accessTokenSecret']

#set oauth stuff
oauth = OAuth1(CONSUMER_KEY,
client_secret=CONSUMER_SECRET,
resource_owner_key=ACCESS_TOKEN,
resource_owner_secret=ACCESS_TOKEN_SECRET)


class MediaTweet(object):

  def __init__(self, file_name, message):
    #twitter endpoints
    MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
    POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

    #read config
    creds = 'credConfig.cfg'
    config = configparser.ConfigParser()
    config.read(creds)
    CONSUMER_KEY = config['twitter']['consumerKey']
    CONSUMER_SECRET = config['twitter']['consumerSecret']
    ACCESS_TOKEN = config['twitter']['accessToken']
    ACCESS_TOKEN_SECRET = config['twitter']['accessTokenSecret']

    #set oauth stuff
    oauth = OAuth1(CONSUMER_KEY,
      client_secret=CONSUMER_SECRET,
      resource_owner_key=ACCESS_TOKEN,
      resource_owner_secret=ACCESS_TOKEN_SECRET)
    
    #image file properties
    self.filename = file_name
    self.total_bytes = os.path.getsize(self.filename)
    self.media_id = None
    self.processing_info = None


  def upload_init(self):
    '''
    Initializes Upload
    '''
    print('INIT')
    self.mime_type = magic.from_file(self.filename, mime=True)
    if self.mime_type.startswith("image"):
        self.media_category = 'tweet_image'
    if self.mime_type.startswith("video"):
        self.media_category = 'tweet_video'
        
    request_data = {
      'command': 'INIT',
      'media_type': self.mime_type,
      'total_bytes': self.total_bytes,
      'media_category': self.media_category
    }
    
    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
    media_id = req.json()['media_id']

    self.media_id = media_id

    #print('Media ID: %s' % str(media_id))


  def upload_append(self):
    '''
    Uploads media in chunks and appends to chunks uploaded
    '''
    segment_id = 0
    bytes_sent = 0
    file = open(self.filename, 'rb')

    while bytes_sent < self.total_bytes:
      chunk = file.read(4*1024*1024)
      
      print('APPEND')

      request_data = {
        'command': 'APPEND',
        'media_id': self.media_id,
        'segment_index': segment_id
      }

      files = {
        'media':chunk
      }
      req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

      if req.status_code < 200 or req.status_code > 299:
        print(req.status_code)
        print(req.text)
        sys.exit(0)

      segment_id = segment_id + 1
      bytes_sent = file.tell()

      #print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

    #print('Upload chunks complete.')


  def upload_finalize(self):
    '''
    Finalizes uploads and starts video processing
    '''
    print('FINALIZE')

    request_data = {
      'command': 'FINALIZE',
      'media_id': self.media_id
    }

    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
    #print(req.json())

    self.processing_info = req.json().get('processing_info', None)
    image_status = self.check_status()
    return image_status

  def check_status(self):
    '''
    Checks media processing status
    '''
    if self.processing_info is None:
      return

    state = self.processing_info['state']

    print('Media processing status is %s ' % state)

    if state == u'succeeded':
      return state

    if state == u'failed':
      return state
      #sys.exit(0)

    check_after_secs = self.processing_info['check_after_secs']
    
    #print('Checking after %s seconds' % str(check_after_secs))
    time.sleep(check_after_secs)

    print('STATUS')

    request_params = {
      'command': 'STATUS',
      'media_id': self.media_id
    }

    req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)
    
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()
    return state

  def tweet(self, message):
    '''
    Publishes Tweet with attached media
    '''
    request_data = {
      'status': message,
      'media_ids': self.media_id
    }

    req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
    #print(req.json())

  def media_main(filename, message):
    mediaTweet = MediaTweet(filename, message)
    mediaTweet.upload_init()
    mediaTweet.upload_append()
    image_status = mediaTweet.upload_finalize()
    #print(image_status)
    if image_status == 'failed':
        return 'failed'
    if image_status == 'pending':
        return 'failed'
    mediaTweet.tweet(message)

if __name__ == '__main__':
    media_main(filename, message)
