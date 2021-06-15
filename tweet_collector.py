import os
import tweepy as tw
import pandas
import sqlite3
import xlwt
from xlwt import Workbook
import sys

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Most important program of the project
#collects tweets for the hashtag given as input
#stores tweets in a Excel file which later wee can use to store the items in the database
#file containg tweets
input_hashtag=sys.argv[1]
print("Collecting tweets for:",input_hashtag)
file=open(str(input_hashtag)+"_tweets.txt","a")
wb=Workbook("Polarization.xls")
row=1
last_row=1
def storeInFile(tweet_id,user_id,user_name,ret,ret_id):
	global file
	tweet_info=str(tweet_id)+'|'+str(user_id)+'|'+user_name+'|'+str(ret_id)+'|'+ret
	file.write(tweet_info)
	file.write('\n')

def storeInExcelSheet(tweet_id,user_id,user_name,ret_id,color,date,tweet_text):
	global row,new_sheet,last_row


	col=1

		#tokens=tokenizer(line)
		#print(tokens[0],tokens[1],tokens[2],tokens[3])

		#tweet_id col
	new_sheet.write(row,col,str(tweet_id))
	col+=1
		#user_id col
	new_sheet.write(row,col,str(user_id))
	col+=1
		#user_name col
	new_sheet.write(row,col,str(user_name))
	col+=1
		#retweer_list col
	new_sheet.write(row,col,str(ret_id))
	col+=1
		#color col
	new_sheet.write(row,col,str(color))
	col+=1

		#date col
	new_sheet.write(row,col,str(date))
	col+=1

		#tweet text col
	new_sheet.write(row,col,str(tweet_text))

	col=1
	row+=1
	wb.save("Polarization.xls")
	last_row+=1

		#line=input_file.readline().strip()
		#print(line)

#Defining personal dev keys
#Fill with your unique key and token from twitter dev
consumer_key=''
consumer_secret_key=''
access_token=''
access_secret_token=''


#Setting up authorization
auth=tw.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_secret_token)
api=tw.API(auth,wait_on_rate_limit=True)



#Retrieve tweets about #covid19

search_words="#"+str(input_hashtag)
date_since="2021-01-01"
tweets=tw.Cursor(api.search,q=search_words,tweet_mode='extended',lang="en",since=date_since).items()
color="Red"
new_sheet=wb.add_sheet("#coronavirus")

#Write the information boxes of the xl sheet
new_sheet.write(0,1,"Tweet id")
new_sheet.write(0,2,"User id")
new_sheet.write(0,3,"User name")
new_sheet.write(0,4,"Retweeter id")
new_sheet.write(0,5,"Color")
new_sheet.write(0,6,"Date")
new_sheet.write(0,7,"Text")


for tw in tweets:
	#print('----------------')
	tweet_id=tw.id
	print(tweet_id)
	#print("Tweeted by:",tw.user.screen_name)
	user_name=tw.user.screen_name
	user_id=tw.user.id
	retweets_list=api.retweeters(tw.id)
	ret=""
	ret_id=""
	for retweet in retweets_list:
		#print('----------------')
		user=api.get_user(retweet)
		#print("Retweed by:",user.screen_name)
		ret+=user.screen_name
		ret+=','
		ret_id+=str(user.id)
		ret_id+=','
	ret=ret[:-1]
	ret_id=ret_id[:-1]
	date=tw.created_at
	#tweet_text=tw.full_text

	if hasattr(tw, "retweeted_status"):  # Check if Retweet
		try:
			tweet_text=tw.retweeted_status.extended_tweet["full_text"]
		except AttributeError:
			tweet_text=tw.retweeted_status.full_text
	else:
		try:
			tweet_text=tw.extended_tweet["full_text"]
		except AttributeError:
			tweet_text=tw.full_text


	print("Ret:",ret)
	print("Ret_id:",ret_id)
	storeInFile(tweet_id,user_id,user_name,ret,ret_id)
	storeInExcelSheet(tweet_id,user_id,user_name,ret_id,color,date,tweet_text)

print(last_row)
