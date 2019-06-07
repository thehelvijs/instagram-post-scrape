from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

username = 'caseyneistat'
post_count = 25

# Allocate chromedriver
browser = webdriver.Chrome('/PATH_TO_CHROMEDRIVER/chromedriver.exe')
browser.get('https://www.instagram.com/'+username+'/?hl=en')

links = []
posts = {}

format_json = {}
like_count = 0
comment_count = 0 
timestamp = 0

# Calculate how many times it needs to scroll to get to bottom
scroll_delay = 2
scroll_amount = round(post_count/(9))
if scroll_amount <= 0:
	scroll_amount = 1

print('It will take about ' + str(round(((scroll_amount*scroll_delay) + (post_count/0.5))/60)) + ' minutes to run this program' )

# Get all links
for i in range(scroll_amount):
	Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(scroll_delay)
	source = browser.page_source
	data=bs(source, 'html.parser')
	body = data.find('body')
	script = body.find('span')
	for link in script.findAll('a'):
		if re.match("/p", link.get('href')):
			links.append('https://www.instagram.com'+link.get('href'))

# Remove duplicates
links = list(set(links))

print('Got ' + str(len(links)) + ' links; getting info')

# Extract info from links
for i in range(len(links)):
	try:
		page = urlopen(links[i]).read()
		data=bs(page, 'html.parser')
		body = data.find('body')
		script = body.find('script')
		raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
		json_data=json.loads(raw)
		posts =json_data['entry_data']['PostPage'][0]['graphql']
		posts= json.dumps(posts)
		posts = json.loads(posts)

		# Check if any of the parameters can be found, if not, set them as 0
		if 'edge_media_preview_like' in str(posts):
			like_count = posts['shortcode_media']['edge_media_preview_like']['count']
		else:
			like_count = 0
		if 'edge_media_preview_comment' in str(posts):
			comment_count = posts['shortcode_media']['edge_media_preview_comment']['count']
		else:
			comment_count = 0
		if 'taken_at_timestamp' in str(posts):
			timestamp = datetime.utcfromtimestamp(posts['shortcode_media']['taken_at_timestamp']).strftime('%Y-%m-%d')
		else:
			timestamp = 0

		# Format JSON
		format_json[str(timestamp)] = {
			'likes' : int(like_count),
			'comments' : int(comment_count)
		}
	except ConnectionResetError:
		print('ConnectionResetError; An existing connection was forcibly closed by the remote host')

print('Writing to ' + username + 'scrape.json')

#Save to .json
try:
	with open(username + 'scrape.json', 'r') as read_data:
		read_data.close()
	with open(username + 'scrape.json', 'w+') as data_file:	
		json.dump(format_json, data_file, indent=3, separators=(',', ': '), sort_keys=True)
		data_file.close()
except:
	with open(username + 'scrape.json', 'w+') as data_file:	
		json.dump(format_json, data_file, indent=3, separators=(',', ': '), sort_keys=True)
		data_file.close()

print('Write successful')
