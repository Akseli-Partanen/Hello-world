import urllib.parse, urllib.request, json
from hashlib import sha1
import hmac
import base64
import time
import random

#Server Links
REQUEST_URL = "https://api.twitter.com/oauth/request_token";
ACCESS_URL = "https://api.twitter.com/oauth/access_token";
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize";

#Consumer keys
TOKEN = "1sRoUXypZA6RpXzUrvIKAEcnk"
TOKEN_SECRET = 'qfGdZ6KcnlVjQHiJKTu3W4QrFxKHi4nSQH5pdjLc78AmfB7VJz'


#Build content header for POST to return request tokens

HEADER_TITLE = "Authorization"

#Consumer key
HEADER = 'OAuth oauth_callback="oob", oauth_consumer_key="' + TOKEN + '", '

#Nonce
HEADER += 'oauth_nonce="'
NONCE = ""
for i in range(32):
	NONCE += chr(random.randint(97, 122))
HEADER += NONCE
HEADER += '", '

#Timestamp
TIMESTAMP = str(int(time.time()))

#Signature
HEADER += 'oauth_signature="'
PARAMETER_STRING = "oauth_callback=oob&oauth_consumer_key=" + TOKEN + "&oauth_nonce=" + NONCE + "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + TIMESTAMP + "&oauth_version=1.0"
BASE_STRING = 'POST&' + urllib.parse.quote(REQUEST_URL, '') + '&' + urllib.parse.quote(PARAMETER_STRING, '')
SIGNING_KEY = urllib.parse.quote(TOKEN_SECRET, '') + '&'
print("DEBUG : SIGNING KEY " + SIGNING_KEY + " BASE STRING " + BASE_STRING + "\n")
HEADER += urllib.parse.quote(base64.standard_b64encode(hmac.new(SIGNING_KEY.encode(), BASE_STRING.encode(), sha1).digest()).decode('ascii'))
HEADER += '", '

#Signature Method
HEADER += 'oauth_signature_method="HMAC-SHA1", '

#Timestamp
HEADER += 'oauth_timestamp="' + TIMESTAMP + '", '

#Version
HEADER += 'oauth_version="1.0"'

print(HEADER_TITLE + ":\n" + HEADER)

HTTP_REQUEST = urllib.request.Request(REQUEST_URL)
HTTP_REQUEST.add_header(HEADER_TITLE, HEADER)
print(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())