import urllib.request
import urllib.parse
import random
import string
import time
import hmac
from hashlib import sha1
import base64
import re

def main():
	
	oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
	oauth_timestamp = str(int(time.time()))
	
	values = {'oauth_token' : getKey(),
				'oauth_consumer_key' : consumerInfo(),
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0'}
	
	vdict = {}
	for key in values:
		vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values[key], safe='')		
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
	
	signing_key = urllib.parse.quote(consumerInfo('secret'), safe='') + '&' + urllib.parse.quote(getKey('secret'), safe='')
	signature = urllib.parse.quote(base64.standard_b64encode(hmac.new(signing_key.encode(), string1.encode(), sha1).digest()).decode('ascii'))
	values['oauth_signature'] = signature

	DST = []
	DST.append('OAuth ')					
	for key in sorted(values):									
		DST.append(urllib.parse.quote(key, safe=''))
		DST.append('="')
		if key == 'oauth_signature':
			DST.append(values[key])
		else:
			DST.append(urllib.parse.quote(values[key], safe=''))
		DST.append('"')
		DST.append(', ')
	DST.pop(-1)
	DST = ''.join(DST)
	'''
	print(DST)
	print(getKey())
	print(getKey("secret"))
	'''
	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/1.1/statuses/home_timeline.json')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
	print(resp)
	
def getKey(type=None):
	fob = open('Tw_secret.txt', 'r')
	lines = fob.readlines()
	fob.close()
	if type is 'secret':
		secret = ''.join(re.findall(r'(.*?)\n', lines[3]))
		return secret
	else:
		token = ''.join(re.findall(r'(.*?)\n', lines[2]))
		return token
	
def consumerInfo(type=None):
	fob = open('Tw_secret.txt', 'r')
	lines = fob.readlines()
	fob.close()
	if type is 'secret':
		consumer_secret = ''.join(re.findall(r'consumer_secret: (.*?)\n', lines[1]))
		return consumer_secret
	else:
		consumer_key = ''.join(re.findall(r'consumer_key: (.*?)\n', lines[0]))
		return consumer_key

if __name__ == '__main__':
    main()