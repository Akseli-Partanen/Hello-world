import json
import webbrowser
import httplib2

from apiclient import discovery
from oauth2client import client

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'

def main():
	flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPES,
												redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	auth_uri = flow.step1_get_authorize_url()
	webbrowser.open(auth_uri)
	
	auth_code = input('Enter the auth code: ')
	
	credentials = flow.step2_exchange(auth_code)
	http_auth = credentials.authorize(httplib2.Http())
	
	calendar_s = discovery.build('calendar', 'v3', http_auth)
	
	events = calendar_s.events().list(calendarId='primary').execute()['items']
	
	for event in events:
		print(event["summary"])

if __name__ == '__main__':
	main()
