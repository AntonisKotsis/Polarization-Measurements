import os
import tweepy as tw
import sqlite3
import networkx as nx

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Purpose of this script is to create a database table
#containing pairs of the original tweet user and all
#the retweeters


#Database credentials
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()


#get all the lines of the database that have at least one retweeter
dataset=cursor.execute("SELECT * FROM coronavirus_table WHERE RETWEET_LIST != ''")


#Creates a list with all the retweeters of each user for a specific tweet
def split_retweeter_list(ret_list):
	new_ret_list_int=[]
	new_ret_list_string=ret_list.split(',')
	for ret in new_ret_list_string:
		int_ret=ret.strip()
		try:
			new_ret_list_int.append(int(int_ret))
		except:
			continue
	return new_ret_list_int



#Creates all the twitter and retweeter pairs
#in other words creates the edges of the retweet graph
def create_user_pairs(initial_user_id,retweeter_list):
	print("init:",initial_user_id)
	for ret in retweeter_list:
		db_connection.execute("INSERT OR IGNORE INTO  retweeters_table (INITIAL_USER_ID,RETWEETER_ID) VALUES (?,?)",(initial_user_id,ret))

	db_connection.commit()



def create_retweet_graph_tables():
	#creates the retweeters table in the database if it's not already been created
	cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='retweeters_table' ''')

	if cursor.fetchone()[0]==1:
		print("Table already exists")
	else:
		db_connection.execute(''' CREATE TABLE retweeters_table
		(INITIAL_USER_ID INT  NOT NULL ,
		RETWEETER_ID INT NOT NULL);''')


	#creates the SUPPORTERS table in the database if it's not already been created
	cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='supporters_table' ''')

	if cursor.fetchone()[0]==1:
		print("Table already exists")
	else:
		db_connection.execute(''' CREATE TABLE supporters_table
		(USER_ID INT PRIMARY KEY NOT NULL );''')


	#creates the DENIERS table in the database if it's not already been created
	cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='deniers_table' ''')

	if cursor.fetchone()[0]==1:
		print("Table already exists")
	else:
		db_connection.execute(''' CREATE TABLE deniers_table
		(USER_ID INT PRIMARY KEY NOT NULL );''')


#Clears every row of the retweeters_table
def clear_retweet_graph_tables():
	db_connection.execute("DELETE FROM retweeters_table")

	db_connection.commit()





#create the retweeters table
#un-comment following line in order to recreate the tables

#create_retweet_graph_tables()


#This must happen every time I collect new data(tweets)
#So I dont have to update the table every single time
#If the choice is YES delete everything in the Retweeters_List and renew it


choice=input("Recreate RETWEETERS_LIST? YES/NO \n")
if(choice=="YES"):
	clear_retweet_graph_tables()
	for row in dataset:
		print("row3",row[3])
		retweeter_list=split_retweeter_list(row[3])
		create_user_pairs(row[1],retweeter_list)






db_connection.close()
