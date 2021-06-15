import sqlite3
import os
import xlrd
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Script that initializes or updates the database
#uses the xl file we created at tweet_collector.py to store tweets in the Database

def initialize_db():
	cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='coronavirus_table' ''')

	if cursor.fetchone()[0]==1:
		print("Table already exists")
	else:
		db_connection.execute(''' CREATE TABLE coronavirus_table
		(TWEET_ID INT PRIMARY KEY NOT NULL ,
		USER_ID INT NOT NULL,
		USER_NAME TEXT NOT NULL,
		RETWEET_LIST TEXT NOT NULL,
		COLOR TEXT NOT NULL);''')

def extract_xl_data(sheet_name):
	#excel file containing tweets
	input_file="Polarization.xls"
	wb=xlrd.open_workbook(input_file)
	pointSheets = wb.sheet_names()
	sheet_index=-1
	tweet_list=[]
	row=1
	col=1
	for i in pointSheets :
		print("Sheet name:",sheet_name)
		sheet_index+=1
		if(i==sheet_name):
			break

	#print("index:",sheet_index)

	sheet=wb.sheet_by_index(sheet_index)

	while(True):
		tokens=[]
		col=1
		if(sheet.cell_value(row,col)=='end'):
			break
		while(col<8):
			tokens.append(sheet.cell_value(row,col))
			#print(sheet.cell_value(row,col))
			col+=1
		tweet_list.append(tokens)
		row+=1


	return tweet_list


def insert_data_to_database(tweet_list):
	for tw in tweet_list:

		db_connection.execute("INSERT OR IGNORE INTO coronavirus_table (TWEET_ID,USER_ID,USER_NAME,RETWEET_LIST,COLOR,DATE_CR,TWEET_TEXT) VALUES (?,?,?,?,?,?,?)",(tw[0],tw[1],tw[2],tw[3],tw[4],tw[5],tw[6]))
		#print("ok")



#=============================#
#when we access the database tables they have the following format
#row[0]->is the Tweet_id
#row[1]->is the User_id
#row[2]->is the User_name
#row[3]->contains the list of user that have retweeted this tweet
#row[4]->color of the user
#row[5]->date of tweet
#row[6]->text of tweet
#=============================#
def show_database():
	cursor.execute("SELECT * FROM coronavirus_table ")
	for row in cursor:
		print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])

initialize_db()
g_tweet_list=extract_xl_data("#coronavirus")
insert_data_to_database(g_tweet_list)

show_database()
db_connection.commit()
db_connection.close()
