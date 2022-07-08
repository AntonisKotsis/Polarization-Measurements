# Polarization-Measurements
Code for my bachelor's thesis with subject: Analyze and Measure Polarization on Covid-19
Implemented using Python.
The main object of the thesis was to prove that Covid-19 is a cotroversial subject by constantly observing Tweets of two Twitter user groups which we called **supporters** and **deniers**. At first we collected data for both groups and stored them in an SQL database we created, this procedure lasted four months so we could have a good amount of data to perform our measurments. Data gathering was performed by a script which used Twitter hashtags in order to locate relevant tweets for each group. Each team had a bunch of different hashtags that they're using and we found out this by manually inspecting a great amount of tweets. For each tweet we collected we kept in the db the following fields: Tweet id, user id, username, hashtag set, retweerers, color.
The color field was applied to each user by the script during the collection process accordingly to the group he belonged and it could take the values red (denier) and blue (supporter).
After that we created a script that generates a new SQL table with user tweets and their retweeters. Each user of this table have been converted lately to a node graph using Gephi. In that graph two well-separated clusters of users have been created with red in one side and blue color at the other, proving that Covid is a controversial subject. To solidify our assumptions we also compared our results with other thesis that studied non-controversial subjects and we took back positive results. In the end we performed measurments in the retweet graph to prove statisticly that our assumptions are correct and we implemented one more graph that contained the hashtags of each set in two clusters. If you need more information about the thesis or you want to read my report please contact me.

**To implement this thesis I was guided and helped by professor Evaggelia Pitoura of the University of Ioannina.**

Pipeline
--------

1)**tweet_collector.py hashtag_name**-> collects tweets for the given hashtag and stores the to an Excel sheet

2)**tweet_db.py**->initializes or updates the database with the tweets from the Excel sheet

3)**addDateColumn.py**->Adds column Date in the database table

4)**addTweetTextColumn.py**->Adds column Tweet_Text in the table

5)**CreateRetweetDataset.py**->Creates pairs of Twitter users (initial user,retweeter)

6)**createSupportersDeniersTable.py**->Creates 2 tables of users, one for each team

7)**createRetweetGraph.py**->Builds the retweet graph and produce a graph file for Gephi

8)**createGraph.py**->Builds the hashtag connection graph and produce a graph file for Gephi

9)**calculateHashtagInjection.py**->Calculates the percentage of users using a hashtag from the opposite hashtag set

10)**calculateHomophily.py**->Calculates the homophily of the retweet graph

11)**calculateConnectionPossibility.py**->Calculates the percentage of nodes which are connected with nodes of the same set


**NOTE**:You have to define your personal key and token from Twitter devs in all scripts that are using tweepy, in order to run the program
