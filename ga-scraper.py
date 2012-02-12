#/usr/bin/python
# GA code - (CC-by) 2010 Copyleft Michal Karzynski, GenomikaStudio.com 

import datetime
import re
import urllib2

from BeautifulSoup import BeautifulSoup
import gdata.analytics.client
import gdata.sample_util
 
GA_USERNAME="rolls707@gmail.com"  # Set these values
GA_PASSWORD="xxxxxxx"
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

query_uri = gdata.analytics.client.DataFeedQuery({
	'ids': GA_PROFILE_ID,
      	'start-date': sd,
      	'end-date': ed,
      	'dimensions': 'ga:date',
      	'metrics': 'ga:visits',
})

feed = gaclient.GetDataFeed(query_uri);


# we'll run through the data feed reutrned from our query
for entry in feed.entry:

	# build each row of data from the feed
      	row = []

	for dim in entry.dimension:
		print dim.value

		for metric in entry.metric:
			print metric.value


page = urllib2.urlopen('http://www.vistaseeker.com')

soup = BeautifulSoup(page)
print soup.find(text=re.compile('friend'))



