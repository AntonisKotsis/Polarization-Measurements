import sqlite3
import tweepy as tw
#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()
update_cursor=db_connection.cursor()

#Defining personal dev keys
consumer_key=''
consumer_secret_key=''
access_token=''
access_secret_token=''

auth=tw.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_secret_token)
api=tw.API(auth,wait_on_rate_limit=True)

#add a column with the full text of the tweet in the coronavirus table
addDTextCol="ALTER TABLE coronavirus_table ADD COLUMN TWEET_TEXT TEXT"
cursor.execute(addDTextCol)

tweets=cursor.execute("SELECT TWEET_ID FROM coronavirus_table")

for row in tweets:

	try:
		tweet=api.get_status(row[0],tweet_mode="extended")
	except:
		continue



	if hasattr(tweet, "retweeted_status"):  # Check if Retweet
		try:
			print(tweet.retweeted_status.extended_tweet["full_text"]+'\n')
			updateAction="UPDATE coronavirus_table SET TWEET_TEXT=(?) WHERE TWEET_ID= (?)"
			update_cursor.execute(updateAction,(tweet.retweeted_status.extended_tweet["full_text"],row[0]))
		except AttributeError:
			print(tweet.retweeted_status.full_text+'\n')
			updateAction="UPDATE coronavirus_table SET TWEET_TEXT=(?) WHERE TWEET_ID= (?)"
			update_cursor.execute(updateAction,(tweet.retweeted_status.full_text,row[0]))
	else:
		try:
			print(tweet.extended_tweet["full_text"]+'\n')
			updateAction="UPDATE coronavirus_table SET TWEET_TEXT=(?) WHERE TWEET_ID= (?)"
			update_cursor.execute(updateAction,(tweet.extended_tweet["full_text"],row[0]))
		except AttributeError:
			print(tweet.full_text+'\n')
			updateAction="UPDATE coronavirus_table SET TWEET_TEXT=(?) WHERE TWEET_ID= (?)"
			update_cursor.execute(updateAction,(tweet.full_text,row[0]))
	db_connection.commit()

db_connection.close()
