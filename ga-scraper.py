#/usr/bin/python
# Fairly useless script to find top keywords in top pageviews 
# GA code - (CC-by) 2010 Copyleft Michal Karzynski, GenomikaStudio.com 

import datetime
import re
from urllib2 import urlopen, URLError

from BeautifulSoup import BeautifulSoup
import gdata.analytics.client
import gdata.sample_util
 
GA_USERNAME="rolls707@gmail.com"  # Set these values
GA_PASSWORD="xxxx"
GA_PROFILE_ID = 'ga:53043715' # the GA profile ID to query
GA_SOURCE_APP_NAME = 'FOO BAR'
sd = datetime.date(2011,12,1)
ed = datetime.date(2012,2,6)

gaclient = gdata.analytics.client.AnalyticsClient(source=GA_SOURCE_APP_NAME)

gaclient.client_login(
        GA_USERNAME,
        GA_PASSWORD,
        GA_SOURCE_APP_NAME,
        service='analytics')

# get the top ten pageviews		
pageviewQuery = gdata.analytics.client.DataFeedQuery({
	'ids': GA_PROFILE_ID,
      	'start-date': sd,
      	'end-date': ed,
      	'dimensions': 'ga:pagePath',
      	'metrics': 'ga:pageviews',
		'sort':'-ga:pageviews',
		'max-results':'25',
})

# get the top ten keyword phrases
kwphrasequery = gdata.analytics.client.DataFeedQuery({
	'ids': GA_PROFILE_ID,
      	'start-date': sd,
      	'end-date': ed,
      	'dimensions': 'ga:keyword',
      	'metrics': 'ga:organicSearches',
		'sort':'-ga:organicSearches',
		'max-results':'200',
})

kwfeed = gaclient.GetDataFeed(kwphrasequery);
feed = gaclient.GetDataFeed(pageviewQuery);

for entry in feed.entry:

	for dim in entry.dimension:
		url = 'http://www.vistaseeker.com' +  dim.value
		print url
		try:
			page = urlopen(url)
			soup = BeautifulSoup(page)
	
			for kwentry in kwfeed.entry:
				for kw in kwentry.dimension:
					try:
						match = soup.findAll(text=re.compile(kw.value))
						
						if len(match) > 0 : 
							print "---------------"
							print url
							print 'Keyword: ' + kw.value
							print 'Matching text: '+ match[0]
							print "---------------"				
						
					except:
						print 'Error at ' + kw.value
						
		except URLError:
			print 'The server couldn\'t fulfill the request.'
		