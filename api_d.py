import urllib.request
import urllib.parse
import simplejson
import re
import time

def main():
	url1 = 'https://accounts.google.com/o/oauth2/device/code'
	values1 = {'client_id' : '1020334559922-mtmhg9iad20brl711ib7eq3s6gdnvjdl.apps.googleusercontent.com',
				'scope' : 'https://www.googleapis.com/auth/calendar.readonly'}

	data = urllib.parse.urlencode(values1)
	data = data.encode('utf-8')
	req = urllib.request.Request(url1,data)
	resp = urllib.request.urlopen(req)
	resp_data = str(resp.read())

	# ''.join(a) makes a list of characters (a) into a string.

	veri_code = ''.join(re.findall(r'"user_code" : "(.*?)"', resp_data))
	veri_url = ''.join(re.findall(r'"verification_url" : "(.*?)"', resp_data))
	dev_code = ''.join(re.findall(r'"device_code" : "(.*?)"', resp_data))

	print(veri_url)
	print(veri_code)




	url2 = 'https://www.googleapis.com/oauth2/v4/token'
	values2 = {'client_id' : '1020334559922-mtmhg9iad20brl711ib7eq3s6gdnvjdl.apps.googleusercontent.com',
				'client_secret' : 'qJ6ii-hcCPL-qtgNS7aB5wfo',
				'code' : dev_code,
				'grant_type' : 'http://oauth.net/grant_type/device/1.0'}


	while True:
		try:
			data = urllib.parse.urlencode(values2)
			data = data.encode('utf-8')
			req = urllib.request.Request(url2, data)
			resp = urllib.request.urlopen(req)
			resp_data = str(resp.read())
			break
		except:
			pass
			
		time.sleep(5)

	r_token = ''.join(re.findall(r'"refresh_token": "(.*?)"', resp_data))
	a_token = ''.join(re.findall(r'"access_token": "(.*?)"', resp_data))

	print(a_token)

	url3 = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

	a_token_h = "Bearer " + a_token
	headers = {}
	headers['Authorization'] = a_token_h

	req = urllib.request.Request(url3, headers=headers)
	resp = urllib.request.urlopen(req)

	#simplejson.load(response) converters url response data into python data (dicts, lists, strings)

	json = simplejson.load(resp)
	events = json["items"]

	for event in events:
		print(event["summary"])

main()