import os
import tweepy as tw
import pandas
import sqlite3
#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Database credentials
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()
c=0
r=cursor.execute("SELECT * FROM coronavirus_table ")
hashtag=input("Insert hashtag of interest:")
hashtag_color=input("Insert hashtag color: ")
reds=0
blues=0
for row in r:
	#print(row[6])
	c+=1
	if(hashtag in str(row[6])):
		if(row[4]=="Red"):
			reds+=1
		else:
			blues+=1

print(c)
print("Blue percentage=",blues/c)
print("Red percentage=",reds/c)

db_connection.close()
