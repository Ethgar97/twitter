from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import csv

#Setting the right variables and conecting to the API
fieldnames = ['UserLoation','UserCountry', 'UserName', 'text']
csv.register_dialect('dialect', delimiter=';', quoting=csv.QUOTE_NONE)
auth = OAuthHandler("t3l8llVayMUCRLwh217fUY1p3", "JwqWePyGZuUJzXaGId7jv2iPe3EmLhkFoIbWBDGTf3W0I89lef")
auth.set_access_token("849205479331033088-WdPOGAMZ7dPLuP7WnpejEN62wEsVzQn", "e3FXvPQeWlmmBQ5ylxTzuCZS6WdpVNLKeG1MYsLwMKpMa")
#Writing the header in the csv file
with open('data.csv', 'w',newline='\n') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='dialect')
	writer.writeheader()
#Setting up the listener and the stream
listener = CSVListener()
stream = Stream(auth, listener)
stream.filter(track=['@realDonaldTrump'])


class CSVListener(StreamListener):
	def on_data(self, data):
		global fieldnames
		# decode from json
		decoded = json.loads(data)
		exportData={}
		# testing if the tweet has an an "place" and an "user" 
		if("user" in decoded and "place" in decoded):
			#testing if we cen use the values,meaning they are not null
			#we need to if clauses here to catch pythons dict errors
			if (decoded['user']['location'] is not None and decoded['place'] is not None):
				#Writing the data into the csv file. We have to encode and Decode here to first 
				#decode the ascii characters thet python can't read e.g. Emojis
				#than we have to convert the byte string into a normal string and last
				#we have to mask the line breaks in the text.
				exportData['UserCountry']=repr(decoded['place']['country_code'].encode('ascii', 'ignore').decode('utf-8'))[1:-1]
				exportData['UserLoation']=repr(decoded['user']['location'].encode('ascii', 'ignore').decode('utf-8'))[1:-1]
				exportData['UserName']=repr(decoded['user']['screen_name'].encode('ascii', 'ignore').decode('utf-8'))[1:-1]
				#in testing sometimes there was a tweet whithout a text...
				if("text" in decoded):
					exportData['text']=repr(decoded['text'].encode('ascii', 'ignore').decode('utf-8'))
				else:
					exportData['text']=None
				#exporting the Data in the console and the csv file
				print(exportData)
				with open('data.csv', 'a',newline='\n') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='dialect', escapechar='\\')
					writer.writerow(exportData)
				return True
			else:
				return True
		else:
			return True
	def on_error(self, status):
		print(status)


