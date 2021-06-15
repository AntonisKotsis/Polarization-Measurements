import sqlite3
import tweepy as tw
#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#This script was built in order to
#add a date column in
#the coronavirus_table

#Defining personal dev keys
consumer_key=''
consumer_secret_key=''
access_token=''
access_secret_token=''

#Setting up authorization
auth=tw.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_secret_token)
api=tw.API(auth)

db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()
update_cursor=db_connection.cursor()

addDateCol="ALTER TABLE coronavirus_table ADD COLUMN DATE_CR TEXT"
cursor.execute(addDateCol)

displayDB="SELECT * FROM coronavirus_table"
db_list=cursor.execute(displayDB)

for row in cursor:

	try:
		tweet=api.get_status(row[0],tweet_mode="extended")
	except:
		continue

	print(tweet.created_at)
	updateAction="UPDATE coronavirus_table SET DATE_CR=(?) WHERE TWEET_ID= (?)"
	update_cursor.execute(updateAction,(tweet.created_at,row[0]))

db_connection.commit()
db_connection.close()
