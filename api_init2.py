from queue import Queue
import threading
import urllib.request
import urllib.parse
import re
import time

def main():
	threads = []	
	while True:
		try:
			x = int(input("How many users?\n"))
			break
		except:
			pass
	for t in range(x):
		thread = myThread(t)
		thread.start()
		threads.append(thread)
		
	for t in threads:
		t.join()
	print("Exiting Main Thread")

class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        print("Starting thread " + str(self.threadID))
        getUser(self.threadID)
        print("Exiting thread " + str(self.threadID))
				
def getUser(threadID):
	url1 = 'https://accounts.google.com/o/oauth2/device/code'
	url2 = 'https://www.googleapis.com/oauth2/v4/token'

	values1 =  {'client_id' : clientInfo(),
					'scope' : 'https://www.googleapis.com/auth/calendar.readonly'}
		
	data = urllib.parse.urlencode(values1)
	data = data.encode('utf-8')
	req = urllib.request.Request(url1,data)
	resp = urllib.request.urlopen(req)
	resp_data = str(resp.read())
	
	#''.join(a) makes a list of characters (a) into a string.
	veri_code = ''.join(re.findall(r'"user_code" : "(.*?)"', resp_data))
	veri_url = ''.join(re.findall(r'"verification_url" : "(.*?)"', resp_data))
	dev_code = ''.join(re.findall(r'"device_code" : "(.*?)"', resp_data))
	
	print(veri_url + " : " + veri_code)
	
	values2 = {'client_id' : clientInfo(),
				'client_secret' : clientInfo('secret'),
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
	
	writeKey(a_token, threadID)
	writeKey(r_token, threadID, 'r')	

docLock = threading.Lock()
		
def writeKey(key, threadID, type='a'):
	docLock.acquire()
	fob = open('secret_doc.txt', 'r')
	lines = fob.readlines()
	fob.close()
	while len(lines) < (2*(threadID + 1) + 2):
		lines.append("\n")
	if type is 'r':
		lines[2*(threadID + 1) + 1] = key + "\n"
	else:
		lines[2*(threadID+ 1)] = key + "\n"
	fob = open('secret_doc.txt', 'w')
	fob.writelines(lines)
	fob.close()	
	docLock.release()
	
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