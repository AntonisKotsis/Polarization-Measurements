import sqlite3

db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

cursor.execute("DROP TABLE hashtag_table")

db_connection.commit()
db_connection.close()