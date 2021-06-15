import os
import tweepy as tw
import sqlite3


#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Database credentials
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()


#get all the lines of the database that have at least one retweeter
dataset=cursor.execute("SELECT * FROM coronavirus_table WHERE RETWEET_LIST != ''")

#Clears every row of the retweeters_table
def clear_supporters_deniers_tables():
	db_connection.execute("DELETE FROM supporters_table")
	db_connection.execute("DELETE FROM deniers_table")
	db_connection.commit()

#Enters data to supporters and deniers tables
def insert_supporters_deniers():
	for row in dataset:
		if(row[4]=='Red'):
			print('denier')
			#insert this user in the deniers_table
			db_connection.execute("INSERT OR IGNORE INTO deniers_table (USER_ID,color) VALUES (?,?)",(row[1],"Red"))
		elif(row[4]=='Blue'):
			print('supp')
			#insert this user in the supporters_table
			db_connection.execute("INSERT OR IGNORE INTO supporters_table (USER_ID,color) VALUES (?,?)",(row[1],"Blue"))
	db_connection.commit()

#only use this once
def addCols():
	cursor.execute("ALTER TABLE supporters_table ADD COLUMN color TEXT")
	cursor.execute("ALTER TABLE deniers_table ADD COLUMN color TEXT")



#addCols()
clear_supporters_deniers_tables()
insert_supporters_deniers()
db_connection.close()
