import urllib.request
import urllib.parse
import random
import string
import time
import hmac
import hashlib
import base64
import re


url = 'https://api.twitter.com/oauth/request_token'

HTTP_method = 'POST'																			#This is PIN based authorization because the device will be a smart mirror with very limited user imput capabilities.
																									#as the directions explain PIN based authorization follows the same steps as twitter sign in but the oauth_callback is
oauth_callback = 'oob'																					#set to 'oob'.
oauth_consumer_key = "1sRoUXypZA6RpXzUrvIKAEcnk"												#This is given in twitter api console
oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))	#42 random alphanumeric characters in a string. i chose 42 cause that how many are in the example
oauth_signature_method = 'HMAC-SHA1'
oauth_timestamp = str(int(time.time()))															#time.time() gives a float of seconds since epoch. to remove decimal point i convert it to an int. Then to a string.
oauth_version = str(1.0)

				
values2 = {'oauth_callback' : oauth_callback,
				'oauth_consumer_key' : oauth_consumer_key,
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : oauth_signature_method,
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : oauth_version}					#realized that oauth_version is optional as explained in the directions

vdict = {}
for key in values2:
	vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values2[key], safe='')
		
parameter_str = []
for key in sorted(vdict):																		#sorted(values2) sorts dictionary keys alphabetically
	parameter_str.append(urllib.parse.quote(key, safe=''))										#urllib.parse.quote(key, safe='') This function percent encodes key
	parameter_str.append('=')
	parameter_str.append(urllib.parse.quote(vdict[key], safe=''))
	parameter_str.append('&')

parameter_str.pop(-1)																			#pop to remove element by index. [-1] is last index.
parameter_str = ''.join(parameter_str)

print(parameter_str + '\n')

string = []
string.append(HTTP_method)
string.append('&')
string.append(urllib.parse.quote(url, safe=''))
string.append('&')
string.append(urllib.parse.quote(parameter_str, safe=''))										#urllib.parse.quote(parameter_str, safe='') percent encodes parameter_str
string = ''.join(string)																		#''.join(string) makes a list of strings (string) into one big string

print(string + '\n')

signing_key = urllib.parse.quote('qfGdZ6KcnlVjQHiJKTu3W4QrFxKHi4nSQH5pdjLc78AmfB7VJz', safe='') + '&'
#print(signing_key)

message = string.encode('utf-8')																#also i dont really understand what this encoding is.
secret = signing_key.encode('utf-8')

signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha1).digest())		#Here is the dreaded hmac sha1 algorithmi. I dont really know how this command words, 
signature = str(signature)																				#and pooped it into this code file. However the signature produced by this does 
oauth_signature = ''.join(re.findall(r"b'(.*?)'", signature))												#look like the signature from the example.
#oauth_signature = str(signature)

DST = []
DST.append('Oauth ')

values = {'oauth_nonce' : oauth_nonce,
				'oauth_callback' : oauth_callback,
				'oauth_signature_method' : oauth_signature_method,
				'oauth_consumer_key' : oauth_consumer_key,
				'oauth_signature' : oauth_signature,
				'oauth_timestamp' : oauth_timestamp}
				#'oauth_version' : oauth_version}

#print('\noauth_timestamp: ' + values['oauth_timestamp'])										#This test program will print the timestamp, signature and nonce just to show you how they look like.
print('oauth_signature: ' + values['oauth_signature'])
#print('oauth_nonce: ' + values['oauth_nonce'] + '\n')
				
for key in sorted(values):																				#Here we are making the header string. Again more percent encoding.
	DST.append(urllib.parse.quote(key, safe=''))
	DST.append('=')
	DST.append('"')
	DST.append(urllib.parse.quote(values[key], safe=''))
	DST.append('"')
	DST.append(',')
	DST.append(' ')
DST.pop(-1)
DST.pop(-1)
DST = ''.join(DST)
	
print('Authorization header:\n' + DST + '\n')													#Also the full header will be printed for so you can se it
headers = {}				
headers['Authorization'] = DST

req = urllib.request.Request(url,data=''.encode('utf-8'),headers=headers)						#We need to put something in the data parameter or else the request will be a GET. So to fix this we put a string of length 0
print(req.get_method() + '\n')																	#Print request method just to make sure it's a POST
try:
	resp = urllib.request.urlopen(req)															#And here comes the 400 error.
	resp_data = str(resp.read())
	print(resp_data)
except Exception as e:
	print(e)
	