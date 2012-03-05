# simple web tracking and redirection via rest server
import web
import uuid
import boto

#Mappings for web.py and any other HTTP related stuff
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
		#?channel='ppc'&campaign='mycampaign'
		i = web.input(channel = 'undefined channel',campaign = 'undefined campaign')
		
		#handy way to get HTTP environment variables
		referer = web.ctx.env.get('HTTP_REFERER', 'undefined referer')		
		
		#get the custId from the cookie or create a new one
		custId = self.HandleCookie(str(uuid.uuid1()))
		#invoke the tracker
		return Tracker().Track(custId,i.channel,i.campaign,referer)
	
	#get/set the master customerId cookie
	def HandleCookie(self,defaultCookieValue):
		cookieName = 'bolCustId'
		cookieDuration = 3600
		
		#see if the user has a custId set in a cookie already, 
		cookie = web.cookies().get(cookieName)					
				
		#set it if they dont	
		if cookie is None:
			web.setcookie(cookieName,defaultCookieValue,cookieDuration)
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

		#connect to dynamoDb	
		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
			
		#create a table if one doesn't already exist	
		try:
			table = conn.get_table('Tracker')
		except:
			table = self.CreateTable(self.tableName, conn)
			
		#save off the new record	
		item = table.new_item(
			hash_key=custId,
			range_key=campaign,
			attrs=self.trackedrows
		)
		
		item.put()
		
		#retrieve and return the item
		return self.GetByUID(custId,campaign)
		
	#creates a tracking table
	def CreateTable(self,tablename, conn):
		if conn is not None:
			table_schema = conn.create_schema(
					hash_key_name='CustomerId',
					hash_key_proto_value='S',
					range_key_name='Campaign',
					range_key_proto_value='S'
			)
		
			table = conn.create_table(
				name=tablename,
				schema=table_schema,
				read_units=10,
				write_units=10
			)	
			
			return table
	
if __name__ == "__main__":
    app.run()