# simple web tracking and redirection via rest server
import web
import uuid
import boto

#Mappings for web.py and any otherHTTP related stuff
urls = (
	'/', 'Status',
	'/track', 'Track',
	'/getbyuid', 'GetByUID',
	)

app = web.application(urls, globals())

class GetByUID:
	def GET(self):
		i = web.input(uid='foo',campaign = 'mycampaign')		
		return Tracker().GetByUID(i.uid,i.campaign)

class Status:
	def GET(self):
		return Tracker().Status()

class Track:
	def GET(self):
		#get the querystring,We expect ?channel='ppc'&campaign='mycampaign&landingpage=foo.bar.com		
		i = web.input(channel = 'undefined channel',campaign = 'undefined campaign')
		referer = web.ctx.env.get('HTTP_REFERER', 'undefined referer')		
		custId = self.HandleCookie(str(uuid.uuid1()))
		#invoke the tracker
		return Tracker().Track(custId,i.channel,i.campaign,referer)
	
	def HandleCookie(self,defaultCookieValue):
		cookieName = 'bolCustId'		
		
		#see qif the user has a custId set in a cookie already, 
		cookie = web.cookies().get(cookieName)					
				
		#set it if they dont	
		if cookie is None:
			web.setcookie(cookieName,custId,3600)
			cookieValue = defaultCookieValue
		else:
			cookieValue = str(cookie)			

		return cookieValue
			
#campaign and customer tracker code
class Tracker:
	awsKeyId = 'xxx'
	awsSecretKey = 'xxx'
	tableName = 'Tracker'
	trackedrows = {}
		
	#returns tracker data for a specific identifier	
	def GetByUID(self, uid, campaign):
		
		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
						
		table = conn.get_table(self.tableName)
		
		item = table.get_item(
			hash_key=str(uid),
			range_key=campaign,
		)
		
		return item
		
	#gets the status of the tracker	
	def Status(self):
		msg = 'Tables: '
		
		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
				
		for table in conn.list_tables():
			msg = conn.describe_table(table)

		return msg		
			
	#tracks some data		
	def Track(self,custId, campaign,channel,referer):
		
		#store it somewhere
		self.trackedrows = {
			'Channel':channel, 
			'Campaign':campaign,
			'Referer' :referer,
		}

		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
			
		try:
			table = conn.get_table('Tracker')
		except:
			self.CreateTable(self.TableName, conn)
			
		item = table.new_item(
			hash_key=custId,
			range_key=campaign,
			attrs=self.trackedrows
		)
		
		item.put()
			
		return self.GetByUID(custId,campaign)
	
	def CreateTable(self,tablename, conn):
		if conn is not none:
			table_schema = conn.create_schema(
					hash_key_name='CustomerId',
					hash_key_proto_value='S',
					range_key_name='Campaign',
					range_key_proto_value='S'
			)
		
			table = conn.create_table(
				name='Tracker',
				schema=table_schema,
				read_units=10,
				write_units=10
			)	
	
if __name__ == "__main__":
    app.run()