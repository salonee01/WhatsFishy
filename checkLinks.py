import requests
import re
import urlexpander
import urlModel
import tldextract
from urllib.parse import urlparse
import time

alert = list()
def check(links):
	for link in links:
		try:
			urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link)
			for url in urls:
				link = url
				originalURL = link
				time_duration = 5
				time_start = time.time()
				while time.time<time_start+duration:
					url = urlexpander.expand(link)
				toBePredicted = [0 for i in range(9)]
				regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}"
				match = re.findall(regex, url)
				domain = urlparse(link).netloc
				if match:
					toBePredicted[0] = -1
				if len(domain) > 25:
					toBePredicted[1] = -1
				if len(domain) <= 20:
					toBePredicted[1] = 1
				else:
					toBePredicted[1] = 1
				if 'tinyurl' in originalURL or 'goo.gl' in originalURL or 'bit.ly' in originalURL:
					toBePredicted[2] = -1
				else:
					toBePredicted[2] = 1
				if '@' in url:
					toBePredicted[3] = -1
				else:
					toBePredicted[3] = 1
				match = re.findall(r"//",url)
				if len(match)>1:
					toBePredicted[4] = -1
				else:
					toBePredicted[4] = 1
				if '-' in url:
					toBePredicted[5] = 0
				result = tldextract.extract(url)
				if result.subdomain:
					toBePredicted[6] = -1
				try:
					response = str(requests.get(url,verify=True))
				except:
					pass
				if response == '<Response [200]>':
					toBePredicted[7] = 1
				else:
					toBePredicted[7] = -1
				if urlparse(link).port:
					toBePredicted[8] = -1
				else:
					toBePredicted[8] = 1
				if urlModel.classifier.predict([toBePredicted]) == -1:
					alert.append(link)
		except:
			pass
	return alert