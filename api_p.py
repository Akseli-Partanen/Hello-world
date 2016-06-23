import urllib.request
import urllib.parse
import simplejson
import re

def main():
	while True:
		user_input = str(input("\n"))
		get_command = re.findall(r'get \d', user_input)
		if len(get_command) == 1:
			user = int(''.join(re.findall(r'\d', ''.join(get_command))))
			if user < userNumber():
				getCalendarEvents(user)
		elif user_input == "refresh":
			pass
		elif user_input == "exit":
			break
		else:
			pass
			
def getCalendarEvents(userID):
	url3 = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
	try:
		a_token_h = "Bearer " + clientToken(userID)
		headers = {}
		headers['Authorization'] = a_token_h
		req = urllib.request.Request(url3, headers=headers)
		resp = urllib.request.urlopen(req)

		#simplejson.load(response) converters url response data into python data (dicts, lists, strings)
		json = simplejson.load(resp)
		events = json["items"]
		for event in events:
			print(event["summary"])
	except:
		refreshAccess(userID)
		try:
			a_token_h = "Bearer " + clientToken(userID)
			headers = {}
			headers['Authorization'] = a_token_h
			req = urllib.request.Request(url3, headers=headers)
			resp = urllib.request.urlopen(req)
			json = simplejson.load(resp)
			events = json["items"]
			for event in events:
				print(event["summary"])
		except Exception as e:
			print(str(e))

def refreshAccess(userID):
	url2 = 'https://www.googleapis.com/oauth2/v4/token'
	
	values2 = {'client_id' : clientInfo(),
				'client_secret' : clientInfo('secret'),
				'refresh_token' : clientToken(userID, 'r'),
				'grant_type' : 'refresh_token'}
	
	try:
		data = urllib.parse.urlencode(values2)
		data = data.encode('utf-8')
		req = urllib.request.Request(url2, data)
		resp = urllib.request.urlopen(req)
		resp_data = str(resp.read())
		
		a_token = ''.join(re.findall(r'"access_token": "(.*?)"', resp_data))
		writeAToken(a_token, userID)
	except Exception as e:
		print(str(e))
	
def clientToken(userID, type='a'):
	fob = open('secret_doc.txt', 'r')
	lines = fob.readlines()
	fob.close()
	if userID > userNumber():
		return 'Error'
	if type is 'r':
		r_token = ''.join(re.findall(r'(.*?)\n', lines[2*(userID + 1) + 1]))
		return r_token
	else:
		a_token = ''.join(re.findall(r'(.*?)\n', lines[2*(userID+ 1)]))
		return a_token
		
def writeAToken(key, userID):
	fob = open('secret_doc.txt', 'r')
	lines = fob.readlines()
	fob.close()
	while len(lines) < (2*(userID + 1) + 2):
		lines.append("\n")	
	lines[2*(userID+ 1)] = key + "\n"
	fob = open('secret_doc.txt', 'w')
	fob.writelines(lines)
	fob.close()
	
def userNumber():
	fob = open('secret_doc.txt', 'r')
	lines = fob.readlines()
	fob.close()
	number = int((len(lines) - 2)/2)
	return number

def clientInfo(type='id'):
	fob = open('secret_doc.txt', 'r')
	lines = fob.readlines()
	fob.close()
	if type is 'secret':
		client_secret = ''.join(re.findall(r'client_secret: (.*?)\n', lines[1]))
		return client_secret
	else:
		client_id = ''.join(re.findall(r'client_id: (.*?)\n', lines[0]))
		return client_id
	
if __name__ == '__main__':
    main()