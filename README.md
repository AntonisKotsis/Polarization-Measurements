# Polarization-Measurements
Code for my bachelor's thesis with subject: Analyze and Measure Polarization on Covid-19
Implemented using Python. The main object of the thesis was to prove that Covid-19 is a cotroversial subject by constantly observing Tweets of two Twitter user groups which we called **supporters** and **deniers**.

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
