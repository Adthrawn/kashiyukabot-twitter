This code is really ugly right now, but I'm going to be cleaning up. 

Currently, this is using a modified, really really dirty version of the Twitter Chunked Upload code. It uses Python 3.x

Some of the values are hard coded right now but I'll move more of them into the cfg file over time to try and make it easier for others to use. 

At the moment, you should only need the following python libraries

 - oauthlib
 - requests
 - requests-oauthlib
 - configparser
 - python3-magic

