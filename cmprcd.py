import urllib.parse, urllib.request
from hashlib import sha1
import hmac
import base64
import time
import random
import string
import re

print("___________________________________________\n")
#Server Links
REQUEST_URL = "https://api.twitter.com/oauth/request_token";

#Consumer keys
TOKEN = "1sRoUXypZA6RpXzUrvIKAEcnk"
TOKEN_SECRET = 'qfGdZ6KcnlVjQHiJKTu3W4QrFxKHi4nSQH5pdjLc78AmfB7VJz'


#Build content header for POST to return request tokens

HEADER_TITLE = "Authorization"

#Consumer key
HEADER = 'OAuth oauth_callback="oob", oauth_consumer_key="' + TOKEN + '", '

#Nonce
HEADER += 'oauth_nonce="'
NONCE = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))

HEADER += NONCE
HEADER += '", '

#Timestamp
TIMESTAMP = str(int(time.time()))

#Signature
HEADER += 'oauth_signature="'
PARAMETER_STRING = "oauth_callback=oob&oauth_consumer_key=" + TOKEN + "&oauth_nonce=" + NONCE + "&oauth_signature_method=HMAC-SHA1&oauth_timestamp=" + TIMESTAMP + "&oauth_version=1.0"
BASE_STRING = 'POST&' + urllib.parse.quote(REQUEST_URL, '') + '&' + urllib.parse.quote(PARAMETER_STRING, '')
SIGNING_KEY = urllib.parse.quote(TOKEN_SECRET, '') + '&'
#print("DEBUG : SIGNING KEY " + SIGNING_KEY + " BASE STRING " + BASE_STRING + "\n")
sig = urllib.parse.quote(base64.standard_b64encode(hmac.new(SIGNING_KEY.encode(), BASE_STRING.encode(), sha1).digest()).decode('ascii'))
HEADER += sig
HEADER += '", '
print(sig)

#Signature Method
HEADER += 'oauth_signature_method="HMAC-SHA1", '

#Timestamp
HEADER += 'oauth_timestamp="' + TIMESTAMP + '", '

#Version
HEADER += 'oauth_version="1.0"'
HEADER = str.strip(HEADER)
print('\n')
print(HEADER_TITLE + ":\n" + HEADER)
'''
HTTP_REQUEST = urllib.request.Request(REQUEST_URL)
HTTP_REQUEST.add_header(HEADER_TITLE, HEADER)
print(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())'''
#__________________________________________________________________________
url = 'https://api.twitter.com/oauth/request_token'

HTTP_method = 'POST'																			

oauth_callback = 'oob'																					
oauth_consumer_key = "1sRoUXypZA6RpXzUrvIKAEcnk"
oauth_nonce = NONCE
oauth_signature_method = 'HMAC-SHA1'
oauth_timestamp = TIMESTAMP
oauth_version = str(1.0)

				
values2 = {'oauth_callback' : oauth_callback,
				'oauth_consumer_key' : oauth_consumer_key,
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : oauth_signature_method,
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : oauth_version}

vdict = {}
for key in values2:
	vdict[urllib.parse.quote(key)] = urllib.parse.quote(values2[key])
		
parameter_str = []
for key in sorted(vdict):
	parameter_str.append(key)	
	parameter_str.append('=')
	parameter_str.append(vdict[key])
	parameter_str.append('&')

parameter_str.pop(-1)
#parameter_str = ''.join(parameter_str)
tparas = ''
for item in parameter_str:
	tparas += item
parameter_str = tparas


string = []
string.append(HTTP_method)
string.append('&')
string.append(urllib.parse.quote(url, safe=''))
string.append('&')
string.append(urllib.parse.quote(parameter_str, safe=''))
#string = ''.join(string)
tstring = ''
for item in string:
	tstring += item
string = tstring


signing_key = urllib.parse.quote('qfGdZ6KcnlVjQHiJKTu3W4QrFxKHi4nSQH5pdjLc78AmfB7VJz', safe='') + '&'

message = string.encode('utf-8')
secret = signing_key.encode('utf-8')

signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), string.encode(), sha1).digest()).decode('ascii'))
print('\n')
print(signature)

DST = []
DST.append('OAuth ')

values = {'oauth_nonce' : oauth_nonce,
				'oauth_callback' : oauth_callback,
				'oauth_signature_method' : oauth_signature_method,
				'oauth_consumer_key' : oauth_consumer_key,
				'oauth_signature' : signature,
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : oauth_version}
	
				
for key in sorted(values):									
	DST.append(urllib.parse.quote(key))
	DST.append('=')
	DST.append('"')
	if values[key] == signature:
		DST.append(signature)
	else:	
		DST.append(urllib.parse.quote(values[key]))
	DST.append('"')
	DST.append(',')
	DST.append(' ')
DST.pop(-1)
DST.pop(-1)
#DST = ''.join(DST)
tDST = ''
for item in DST:
	tDST += item
DST = tDST
	
print('\nAuthorization:\n' + DST)				
headers = {}				
headers['Authorization'] = DST
print('\n' + str(sig == signature))

header = str.split(HEADER)
dst = str.split(DST)

comp = []
for i in range(len(dst)):
	comp.append(dst[i]==header[i])
print('\n')
print(comp)


print(HEADER == DST)
HTTP_REQUEST = urllib.request.Request(url)
HTTP_REQUEST.add_header(HEADER_TITLE, DST)
print(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read()) 
