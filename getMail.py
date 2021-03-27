from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import base64 
import email 
import csv
import nltk
import re
import checkMail
import sendMail
import checkLinks
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import multiprocessing
import time

# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify'] 
  
def getEmails(): 
	# Variable creds will store the user access token. 
	# If no valid token found, we will create one. 
	creds = None
  
	# The file token.pickle contains the user access token. 
	# Check if it exists 
	if os.path.exists('token.pickle'): 
  
		# Read the token from the file and store it in the variable creds 
		with open('token.pickle', 'rb') as token: 
			creds = pickle.load(token) 
  
	# If credentials are not available or are invalid, ask the user to log in. 
	if not creds or not creds.valid: 
		if creds and creds.expired and creds.refresh_token: 
			creds.refresh(Request()) 
		else: 
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
			creds = flow.run_local_server(port=8080) 
  
		# Save the access token in token.pickle file for the next run 
		with open('token.pickle', 'wb') as token: 
			pickle.dump(creds, token) 
  
	# Connect to the Gmail API 
	service = build('gmail', 'v1', credentials=creds) 
	res = service.users().getProfile(userId= 'me').execute()
  
	# request a list of all the messages 
	result = service.users().messages().list(userId='me',maxResults = 10, q='is:unread').execute() 

	messages = result.get('messages')
	# messages is a list of dictionaries where each dictionary contains a message id. 
	# iterate through all the messages 
	mail = dict()
	for msg in messages: 
		# Get the message from its id 
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()
		try: 
			# Get value of 'payload' from dictionary 'txt' 
			payload = txt['payload'] 
			headers = payload['headers']
			# Look for Subject and Sender Email in the headers 
			for d in headers:
				# print(d)
				if d['name'] == 'Subject': 
					subject = d['value'] 
				if d['name'] == 'From': 
					sender = d['value'] 
			print("Checking message with subject:",subject.strip())
			# The Body of the message is in Encrypted format. So, we have to decode it. 
			# Get the data and decode it with base 64 decoder. 
			part = payload.get('parts')[0]
			data = part['body']['data'] 
			data = data.replace("-","+").replace("_","/") 
			decoded_data = base64.b64decode(data) 
  
			# Now, the data obtained is in lxml. So, we will parse  
			# it with BeautifulSoup library 
			soup = BeautifulSoup(decoded_data , "lxml") 
			body = soup.body() 
			body = str(body[0])
			mailFlag = checkMail.check(body)

			art = payload.get('parts')[1]
			data = art['body']['data'] 
			data = data.replace("-","+").replace("_","/") 
			decoded_data = base64.b64decode(data)
			soup = BeautifulSoup(decoded_data , "lxml")
			body = soup.body() 
			domains = set()
			hyperlinks = list()
			for a in soup.find_all('a', href=True):
				hyperlinks.append(a['href'].strip())
				domains.add(urlparse(a['href']).netloc)
			suspiciousLinks = checkLinks.check(hyperlinks)
			if mailFlag == 0 or len(domains)>2 or len(suspiciousLinks)>(len(hyperlinks)//2):
				service.users().messages().trash(userId='me', id=msg['id']).execute()
				mail[sender] = subject	
		except: 
			if mailFlag == 0:
				service.users().messages().trash(userId='me', id=msg['id']).execute()	
				mail[sender] = subject
	sendMail.send(res['emailAddress'], mail)

