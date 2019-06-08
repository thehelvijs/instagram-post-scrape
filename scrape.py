import sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

location = 'data/'
username = input('Username: ')
post_count = input("Post count (write 'all' to scrape all posts): ")

# Locate chromedriver
browser = webdriver.Chrome('C:/Users/Helvijs Adams/Desktop/chromedriver/chromedriver.exe')
browser.get('https://www.instagram.com/'+username+'/?hl=en')

raw = False
raw_data = []
links = []
posts = {}
format_json = {}

# Scrape basic data
post_amount = browser.find_element_by_class_name("g47SY").text
followers = browser.find_element_by_css_selector("a[href*='followers'] span").get_attribute('title')
following = browser.find_element_by_css_selector("a[href*='following'] span").text

if post_count == 'all':
	post_count = int(post_amount.replace(',',''))
else:
	post_count = int(post_count)

# Calculate how many times it needs to scroll to get to bottom
scroll_delay = 5
scroll_amount = round(post_count/(12))
if scroll_amount < 1:
	scroll_amount = 1

print()
print('It will take about ' + str(round(((scroll_amount*scroll_delay) + (post_count*0.85))/60)) + ' minutes to run this program' )
start = time.time()

# Add progress bar
printProgressBar(0, scroll_amount, prefix = '', suffix = 'Collecting links', bar_length = 40)
barcount = 0
# Get all links
for i in range(scroll_amount):
	barcount += 1
	printProgressBar(barcount, scroll_amount, prefix = '', suffix = 'Collecting links', bar_length = 40)
	try:
		Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(scroll_delay)
		source = browser.page_source
		data=bs(source, 'html.parser')
		body = data.find('body')
		script = body.find('span')
		for link in script.findAll('a'):
			if re.match("/p", link.get('href')):
				links.append('https://www.instagram.com'+link.get('href'))
				link_count += 1
	except:
		pass

# Remove duplicates
links = list(set(links))

print()
print('Got ' + str(len(links)) + ' links; extracting data')

# Add progress bar
printProgressBar(0, len(links), prefix = '', suffix = 'Extracting data', bar_length = 40)
barcount = 0
# Extract info from links
for i in range(len(links)):
	barcount += 1
	printProgressBar(barcount, len(links), prefix = '', suffix = 'Extracting data', bar_length = 40)
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

		if raw == True:
			raw_data.append(posts)

		# Check if any of the parameters can be found, if not, set them as None (null)
		# Likes
		if 'edge_media_preview_like' in str(posts):
			like_count = posts['shortcode_media']['edge_media_preview_like']['count']
		else:
			like_count = None
		# Comments
		if 'edge_media_preview_comment' in str(posts):
			comment_count = int(posts['shortcode_media']['edge_media_preview_comment']['count'])
		elif 'edge_media_to_parent_comment' in str(posts):
			comment_count = int(posts['shortcode_media']['edge_media_to_parent_comment']['count'])
		elif 'edge_media_to_comment' in str(posts):
			comment_count = int(posts['shortcode_media']['edge_media_to_comment']['count'])
		else:
			comment_count = None
		# Video
		if 'video_view_count' in str(posts):
			video_view_count = int(posts['shortcode_media']['video_view_count'])
			video_duration = int(posts['shortcode_media']['video_duration'])
		else:
			video_view_count = None
			video_duration = None
		# Timestamp
		if 'taken_at_timestamp' in str(posts):
			timestamp = datetime.utcfromtimestamp(posts['shortcode_media']['taken_at_timestamp']).strftime('%Y-%m-%d')

		# Format JSON
		format_json[str(timestamp)] = {
			'likes' : like_count,
			'comments' : comment_count,
			'video_view_count' : video_view_count,
			'video_duration' : video_duration
		}

	except:
		pass

print()
print('Saving to ' + location + username + '_scrape.json')

#Save to .json
try:
	with open(location + username + '_scrape.json', 'r') as read_data:
		read_data.close()
	with open(location + username + '_scrape.json', 'w+') as data_file:	
		json.dump(format_json, data_file, indent=3, separators=(',', ': '), sort_keys=True)
		data_file.close()
	if raw == True:
		with open(location + username + '_raw.json', 'r') as read_data:
			read_data.close()
		with open(location + username + '_raw.json', 'w+') as data_file:	
			json.dump(raw_data, data_file, indent=3, separators=(',', ': '), sort_keys=True)
			data_file.close()
except:
	with open(location + username + '_scrape.json', 'w+') as data_file:	
		json.dump(format_json, data_file, indent=3, separators=(',', ': '), sort_keys=True)
		data_file.close()
	if raw == True:
		with open(location + username + '_raw.json', 'w+') as data_file:	
			json.dump(raw_data, data_file, indent=3, separators=(',', ': '), sort_keys=True)
			data_file.close()

end = time.time()

print('Scrape successful')
print('Scrape duration: ' + str(datetime.utcfromtimestamp(end-start).strftime('%Hh %Mm')))
