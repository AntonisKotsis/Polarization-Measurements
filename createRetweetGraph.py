import os
import tweepy as tw
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import metis
from fa2 import ForceAtlas2

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#Creates the retweet graph
#Partitions the graph using Metis and color attr


G=nx.Graph()
#Database credentials
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

#nodes
supporters=[]
deniers=[]
supporters_list=[]
deniers_list=[]
#edges
edges=[]

#contains all the users from the database that have tweeted at least once
all_users_list=[]


def getAllUsers():
	global all_users_list
	all_users=db_connection.execute("SELECT USER_ID FROM coronavirus_table")
	#transform the tuple we get to a list
	for i in all_users:
		all_users_list.append(i[0])


def getRetweetGraphData():
	global supporters,deniers,edges

	supporters=db_connection.execute("SELECT * FROM supporters_table")
	deniers=db_connection.execute("SELECT * FROM deniers_table")
	edges=db_connection.execute("SELECT * FROM retweeters_table")
	#print(edges)
	tokenizeTuple(supporters,deniers)



def tokenizeTuple(Supporters,Deniers):
	for sup in Supporters:
		supporters_list.append(sup[0])
	for den in Deniers:
		deniers_list.append(den[0])

	for sup in Supporters:
		print(sup)




#returns the color of each user
def getUserColor(user):
	global all_users_list
	if(user in all_users_list):
			cur_com=cursor.execute("SELECT COLOR FROM coronavirus_table WHERE USER_ID=(?)",(user,))
			user_color=cursor.fetchone()
		#	print(user_color[0])
			return user_color[0]
	return 'Red'



#function that creates the retweet graph
def createPartitionsForGephi():
	global supporters,deniers,edges,supporters_list,deniers_list
	G.add_edges_from(edges)


	#gets the pairs of users
	#edge[0]=initial tweet user
	#edge[1]=retweeter
	edges_in=db_connection.execute("SELECT * FROM retweeters_table")

	all_nodes=[]
	for edge in edges_in:
		#print(edge[0],edge[1])
		all_nodes.append(edge[0])
		all_nodes.append(edge[1])

	for i,v in enumerate(all_nodes):
		#vale to xrwma kathe node gia partion xwris metis
		user_color=getUserColor(v)
		if(user_color=='Blue'):
			G.nodes[v]['node_value']=1
			G.nodes[v]['color']='blue'
		else:
			G.nodes[v]['node_value']=-1
			G.nodes[v]['color']='red'




	G.graph['node_weight_attr'] = 'node_value'
	#metis graph
	G1=metis.networkx_to_metis(G)
	#Get the two partitions from METIS
	(cut, parts) = metis.part_graph(G1, 2)
	colors = ['red', 'blue']
	#print("parts",parts)
	#print(cut)
	for i,p in enumerate(parts):
		G1.node[i]['color']=colors[p]
	nx.write_gexf(G,"NoMetisPart.gexf")
	nx.write_gexf(G1, "MetisPart.gexf")


def dateTokenizer(date):

	new_date=date.split()
	temp=new_date[0].split('-')
	month=temp[1]
	return month

#For future research on monthly polarity measurements
def createMontlyPolarityGraph():
	target_month=0
	target_month=input("Enter targe month:")
	r=cursor.execute("SELECT * FROM coronavirus_table WHERE RETWEET_LIST !=''")
	monthly_tweet=[]
	monthly_graph_edges=[]
	all_nodes=[]
	for row in r:
		if(row[5]!=None):
			date=dateTokenizer(row[5])
			if(date==str(target_month)):
				monthly_tweet.append(row)

	for m in monthly_tweet:
		ret_list=m[3].split(',')
		for ret in ret_list:
			monthly_graph_edges.append((m[1],ret))
	counter=0

	for m in monthly_graph_edges:
		counter+=1
		#print(m)
	print(counter)

	G.add_edges_from(monthly_graph_edges)
	for edge in monthly_graph_edges:
		all_nodes.append(edge[0])
		all_nodes.append(edge[1])

	for i,v in enumerate(all_nodes):

		user_color=getUserColor(v)
		if(user_color=='Blue'):
			G.nodes[v]['node_value']=1
			G.nodes[v]['color']='blue'
		else:
			G.nodes[v]['node_value']=-1
			G.nodes[v]['color']='red'



	G.graph['node_weight_attr'] = 'node_value'
	#Get at MOST two partitions from METIS
	(cut, parts) = metis.part_graph(G, 2)
	colors = ['red', 'blue']

	nx.write_gexf(G, str(target_month)+".gexf")





getAllUsers()
getRetweetGraphData()
createPartitionsForGephi()

#ans=input("Create monthly graph:(yes/no)")
#if(ans=='yes'):
#	createMontlyPolarityGraph()
