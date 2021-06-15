import os
import tweepy as tw
import sqlite3
import networkx as nx

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#


hashtag_file=open("hashtags_file.txt","w")

#gets a dictionary which contains all the information needed for
#the hashtags of a tweet
#and returns just the hashtags in a list
def extractHashtags(hashtags_infos):
	hashtags_list=[]
	for h in hashtags_infos:
		hashtags_list.append(h['text'])
	return hashtags_list

#This table contains pairs of hashtags which are connected
#The EDGE_WEIGHT refers to the numbers of times these 2 hashtags are posted together
def createHashtagTable():
	cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hashtag_table' ''')

	if cursor.fetchone()[0]==1:
		print("Table already exists")
	else:
		db_connection.execute(''' CREATE TABLE hashtag_table
		(HASHTAG_NODE1 TEXT  NOT NULL ,
		HASHTAG_NODE2 TEXT NOT NULL,
		EDGE_WEIGHT INT NOT NULL);''')


def storeHashtagNodes():
	global hashtags_weights,supporters_hashtags,deniers_hashtags,db_connection,supporters_hashtags_weights,deniers_hashtags_weights
	for i in range(len(supporters_hashtags)):
		for j in range (len(deniers_hashtags)):
			db_connection.execute("INSERT OR IGNORE INTO hashtag_table (HASHTAG_NODE1,HASHTAG_NODE2,EDGE_WEIGHT) VALUES (?,?,?)",(supporters_hashtags[i],deniers_hashtags[j],hashtags_weights[i][j]))

	for i in range(len(supporters_hashtags)):
		for j in range (len(supporters_hashtags)):
			db_connection.execute("INSERT OR IGNORE INTO hashtag_table (HASHTAG_NODE1,HASHTAG_NODE2,EDGE_WEIGHT) VALUES (?,?,?)",(supporters_hashtags[i],supporters_hashtags[j],supporters_hashtags_weights[i][j]))

	for i in range(len(deniers_hashtags)):
		for j in range (len(deniers_hashtags)):
			db_connection.execute("INSERT OR IGNORE INTO hashtag_table (HASHTAG_NODE1,HASHTAG_NODE2,EDGE_WEIGHT) VALUES (?,?,?)",(deniers_hashtags[i],deniers_hashtags[j],deniers_hashtags_weights[i][j]))


def showDatabaseHashtagTable():
	cursor.execute("SELECT * FROM hashtag_table ")
	for row in cursor:
		print(row[0],row[1],row[2])
		print('----------------------------------------')
	for row in cursor:
		hashtag_file.write(row[0]+","+row[1]+","+row[2]+"\n")
	hashtag_file.close()

#Database credentials
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

#Lists which contain the hashtags of the 2 clusters
supporters_hashtags=['coronavirus','CoronaVaccine','COVIDSecondWave','COVID19','SocialDistancing','MaskUp']
deniers_hashtags=['Antilockdown','antivaxxers','KBF','Antilockdownprotest','antimask','BellsPalsy','plandemic']


#Defining personal dev keys
#Fill with your unique key and token from twitter dev
consumer_key=''
consumer_secret_key=''
access_token=''
access_secret_token=''


#Setting up authorization
auth=tw.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_secret_token)
api=tw.API(auth)

#this list refers to supporters-deniers hashtags relationship
hashtags_weights=[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

supporters_hashtags_weights=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
deniers_hashtags_weights=[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]



count=0
cr=cursor.execute("SELECT * FROM coronavirus_table ")
#print(cr)
for row in cursor:
	print(row[0])

	hashtags_list=[]
	hashtags_infos=[]
	try:
		tweet=api.get_status(row[0],tweet_mode="extended")
	#the following except was written just in case that
	#a user has deleted a tweet that has already been collected
	except:
		continue

	try:
		#This part refers to tweets which are retweets
		#and they have the attr retweeted_status
		#print(tweet.retweeted_status.full_text)
		hashtags_infos=tweet.retweeted_status.entities.get('hashtags')
		hashtags_list=extractHashtags(hashtags_infos)
		print(hashtags_list)
		for i in range(len(supporters_hashtags)):
			for j in range(len(deniers_hashtags)):
				if(supporters_hashtags[i] in hashtags_list):
					if(deniers_hashtags[j] in hashtags_list):
						hashtags_weights[i][j]+=1


		for i in range(len(supporters_hashtags)):
			for j in range(len(supporters_hashtags)):
				if(supporters_hashtags[i] in hashtags_list):
					if(supporters_hashtags[j] in hashtags_list ):
						supporters_hashtags_weights[i][j]+=1

		for i in range(len(deniers_hashtags)):
			for j in range(len(deniers_hashtags)):
				if(deniers_hashtags[i] in hashtags_list):
					if(deniers_hashtags[j] in hashtags_list ):
						deniers_hashtags_weights[i][j]+=1

	except AttributeError:
		#This part refers to initial tweets
		hashtags_infos=tweet.entities.get('hashtags')
		hashtags_list=extractHashtags(hashtags_infos)
		print(hashtags_list)
		for i in range(len(supporters_hashtags)):
			for j in range(len(deniers_hashtags)):
				if(supporters_hashtags[i] in hashtags_list):
					if(deniers_hashtags[j] in hashtags_list):
						hashtags_weights[i][j]+=1


		for i in range(len(supporters_hashtags)):
			for j in range(len(supporters_hashtags)):
				if(supporters_hashtags[i] in hashtags_list):
					if(supporters_hashtags[j] in hashtags_list ):
						supporters_hashtags_weights[i][j]+=1

		for i in range(len(deniers_hashtags)):
			for j in range(len(deniers_hashtags)):
				if(deniers_hashtags[i] in hashtags_list):
					if(deniers_hashtags[j] in hashtags_list ):
						deniers_hashtags_weights[i][j]+=1

	#print(row[0])
	count+=1
	#dhladh edges apo ton node px coronavirus->coronavirus
	for i in range(len(supporters_hashtags)):
			for j in range(len(supporters_hashtags)):
				if(i==j):
					supporters_hashtags_weights[i][j]=0

	for i in range(len(deniers_hashtags)):
			for j in range(len(deniers_hashtags)):
				if(i==j):
					deniers_hashtags_weights[i][j]=0


print(count)
print(hashtags_weights)
createHashtagTable()
storeHashtagNodes()
db_connection.commit()
showDatabaseHashtagTable()
db_connection.close()
