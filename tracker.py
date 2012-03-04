# simple web tracking and redirection via rest server

import web
import uuid

urls = (
	'/', 'Status',
	'/track', 'Track',
	'/clear', 'Clear')

app = web.application(urls, globals())

class Track:
	def GET(self):
		return Tracker().Track()

class Tracker:

	trackedrows = []

	def Clear(self):
		self.trackedrows = []

	def Status(self):
		return self.trackedrows

	def Track(self):
		cookieName = 'bolCustId'		
		custId = uuid.uuid1()

		#see if the user has a custId set in a cookie already, 
		cookie = web.cookies().get(cookieName)					
		
		#set it if they dont	
		if cookie is None:
			web.setcookie(cookieName,custId,3600)
		else:
			custId = cookie		
	
		#get the querystring,We expect ?channel='ppc'&campaign='mycampaign&landingpage=foo.bar.com		
		i = web.input(channel = 'undefined channel',campaign = 'undefined campaign')
		referer = web.ctx.env.get('HTTP_REFERER', 'undefined referer')		

		#store it somewhere
		self.trackedrows.append({
			"CustId":custId, 
			"Channel":i.channel, 
			"Campaign":i.campaign,
			"Referer" : referer,
		})	
		
		return self.Status()			


if __name__ == "__main__":
    app.run()
