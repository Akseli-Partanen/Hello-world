import urllib.request
import urllib.parse
import random
import string
import time
import hmac
from hashlib import sha1
import base64
import re

#Step 1
consumer_key = "1sRoUXypZA6RpXzUrvIKAEcnk"
consumer_secret = 'qfGdZ6KcnlVjQHiJKTu3W4QrFxKHi4nSQH5pdjLc78AmfB7VJz'

HTTP_method = 'POST'																			
oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
oauth_timestamp = str(int(time.time()))

values2 = {'oauth_callback' : 'oob',
				'oauth_consumer_key' : consumer_key,
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0'}

vdict = {}
for key in values2:
	vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values2[key], safe='')		
parameter_str = []
for key in sorted(vdict):
	parameter_str.append(key)	
	parameter_str.append('=')
	parameter_str.append(vdict[key])
	parameter_str.append('&')
parameter_str.pop(-1)
parameter_str = ''.join(parameter_str)

string1 = []
string1.append(HTTP_method)
string1.append('&')
string1.append(urllib.parse.quote('https://api.twitter.com/oauth/request_token', safe=''))
string1.append('&')
string1.append(urllib.parse.quote(parameter_str, safe=''))
string1 = ''.join(string1)

signing_key = urllib.parse.quote(consumer_secret, safe='') + '&'
signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), string1.encode(), sha1).digest()).decode('ascii'))

values2['oauth_signature'] = signature

DST = []
DST.append('OAuth ')					
for key in sorted(values2):									
	DST.append(urllib.parse.quote(key, safe=''))
	DST.append('="')
	if key == 'oauth_signature':
		DST.append(values2[key])
	else:
		DST.append(urllib.parse.quote(values2[key], safe=''))
	DST.append('"')
	DST.append(', ')
DST.pop(-1)
DST = ''.join(DST)

HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/request_token')
HTTP_REQUEST.add_header("Authorization", DST)
resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())

#Step 2
oauth_token = ''.join(re.findall(r"n=(.*?)&", resp))
oauth_token_secret = ''.join(re.findall(r"t=(.*?)&", resp))
resp_url = 'https://api.twitter.com/oauth/authenticate' + '?' + ''.join(re.findall(r"b'(.*?)&", resp))
print('\n' + resp_url)

PIN = input("input key here:")
oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
oauth_timestamp = str(int(time.time()))

values2 = {'oauth_token' : oauth_token,
				'oauth_consumer_key' : consumer_key,
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0',
				'oauth_verifier' : PIN}

vdict = {}
for key in values2:
	vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values2[key], safe='')		
parameter_str = []
for key in sorted(vdict):
	parameter_str.append(key)	
	parameter_str.append('=')
	parameter_str.append(vdict[key])
	parameter_str.append('&')
parameter_str.pop(-1)
parameter_str = ''.join(parameter_str)

string1 = []
string1.append(HTTP_method)
string1.append('&')
string1.append(urllib.parse.quote('https://api.twitter.com/oauth/access_token', safe=''))
string1.append('&')
string1.append(urllib.parse.quote(parameter_str, safe=''))
string1 = ''.join(string1)

signing_key = urllib.parse.quote(consumer_secret, safe='') + '&' + urllib.parse.quote(oauth_token_secret, safe='')
signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), string1.encode(), sha1).digest()).decode('ascii'))
values2['oauth_signature'] = signature

DST = []
DST.append('OAuth ')					
for key in sorted(values2):									
	DST.append(urllib.parse.quote(key, safe=''))
	DST.append('="')
	if key == 'oauth_signature':
		DST.append(values2[key])
	else:
		DST.append(urllib.parse.quote(values2[key], safe=''))
	DST.append('"')
	DST.append(', ')
DST.pop(-1)
DST = ''.join(DST)
try:
	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/access_token')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
	print('\n' + resp)
except Exception as e:
	print(e)

#Step3
print('\n' + 'check' + '\n')
oauth_token = ''.join(re.findall(r"n=(.*?)&", resp))
oauth_token_secret = ''.join(re.findall(r"t=(.*?)&", resp))

oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
oauth_timestamp = str(int(time.time()))

values2 = {'oauth_token' : oauth_token,
				'oauth_consumer_key' : consumer_key,
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0'}

vdict = {}
for key in values2:
	vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values2[key], safe='')		
parameter_str = []
for key in sorted(vdict):
	parameter_str.append(key)	
	parameter_str.append('=')
	parameter_str.append(vdict[key])
	parameter_str.append('&')
parameter_str.pop(-1)
parameter_str = ''.join(parameter_str)

string1 = []
string1.append('GET')
string1.append('&')
string1.append(urllib.parse.quote('https://api.twitter.com/1.1/statuses/home_timeline.json', safe=''))
string1.append('&')
string1.append(urllib.parse.quote(parameter_str, safe=''))
string1 = ''.join(string1)

signing_key = urllib.parse.quote(consumer_secret, safe='') + '&' + urllib.parse.quote(oauth_token_secret, safe='')
signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), string1.encode(), sha1).digest()).decode('ascii'))
values2['oauth_signature'] = signature

DST = []
DST.append('OAuth ')					
for key in sorted(values2):									
	DST.append(urllib.parse.quote(key, safe=''))
	DST.append('="')
	if key == 'oauth_signature':
		DST.append(values2[key])
	else:
		DST.append(urllib.parse.quote(values2[key], safe=''))
	DST.append('"')
	DST.append(', ')
DST.pop(-1)
DST = ''.join(DST)
print(DST)
try:
	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/1.1/statuses/home_timeline.json')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
	print('\n' + resp)
except Exception as e:
	print(e)
	