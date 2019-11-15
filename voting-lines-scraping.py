import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from datetime import datetime



def votingWaitTimes():
	url = 'https://countyclerk.traviscountytx.gov/elections/current-election.html'
	reqs = requests.Session()

	response = reqs.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	for iframe in soup.select('iframe'):
		if "livevoterturnout" in iframe['src']:
			try:
				response_frame = reqs.get(iframe['src'], verify=False)
			except requests.exceptions.ConnectionError as e:
				response_frame = "No response"
			iframe_soup = BeautifulSoup(response_frame.content, "html.parser")
			
			#wait time at FAC
			flawn = iframe_soup.body.find(text=re.compile('UT Flawn Academic Center'))
			flawn_wait_time = flawn.parent.nextSibling.contents;

			# get wait time from pcl as well when it is available on the site

			#when table was refreshed
			refreshed = iframe_soup.find("span", { "id" : "refreshTimeLab" })
			tr_refreshed = refreshed.parent.parent.nextSibling;
			td_time = tr_refreshed.find('td').string
			dt_refreshed = datetime.strptime(str(datetime.now().year) + ' ' + td_time, '%Y %a %b %d %H:%M %p')
			
			return flawn_wait_time, dt_refreshed
		

print(votingWaitTimes())