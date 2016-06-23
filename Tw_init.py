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
	#Step1
	oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
	oauth_timestamp = str(int(time.time()))
	
	values = {'oauth_callback' : 'oob',
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
	string1.append('POST')
	string1.append('&')
	string1.append(urllib.parse.quote('https://api.twitter.com/oauth/request_token', safe=''))
	string1.append('&')
	string1.append(urllib.parse.quote(parameter_str, safe=''))
	string1 = ''.join(string1)
	
	signing_key = urllib.parse.quote(consumerInfo('secret'), safe='') + '&'
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

	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/request_token')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
	
	oauth_token = ''.join(re.findall(r"n=(.*?)&", resp))
	oauth_token_secret = ''.join(re.findall(r"t=(.*?)&", resp))
	writeTwKey(oauth_token)
	writeTwKey(oauth_token_secret, 's')
	resp_url = 'https://api.twitter.com/oauth/authenticate' + '?' + ''.join(re.findall(r"b'(.*?)&", resp))
	print('\n' + resp_url)
	
	#Step2
	PIN = input("input key here:")
	oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
	oauth_timestamp = str(int(time.time()))
	
	values = {'oauth_token' : oauth_token,
				'oauth_consumer_key' : consumerInfo(),
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0',
				'oauth_verifier' : PIN}

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
	string1.append('POST')
	string1.append('&')
	string1.append(urllib.parse.quote('https://api.twitter.com/oauth/access_token', safe=''))
	string1.append('&')
	string1.append(urllib.parse.quote(parameter_str, safe=''))
	string1 = ''.join(string1)
	
	signing_key = urllib.parse.quote(consumerInfo('secret'), safe='') + '&' + urllib.parse.quote(oauth_token_secret, safe='')
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

	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/access_token')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())

	writeTwKey(''.join(re.findall(r"n=(.*?)&", resp)))
	writeTwKey(''.join(re.findall(r"t=(.*?)&", resp)), 's')

def writeTwKey(key, type='o'):
	fob = open('Tw_secret.txt', 'r')
	lines = fob.readlines()
	fob.close()
	while len(lines) < 4:
		lines.append("\n")
	if type is 's':
		lines[3] = key + "\n"
	else:
		lines[2] = key + "\n"
	fob = open('Tw_secret.txt', 'w')
	fob.writelines(lines)
	fob.close()		
	
def consumerInfo(type='key'):
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
