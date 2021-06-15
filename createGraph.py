import os
import tweepy as tw
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import metis

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

#Returns a List with edges of Hashtags
def getHashTagGraphEdges():
	#Contains all the pairs of hashtags
	#which represent the edge of our hashtag graph
	hashtag_edges=[]
	cursor.execute("SELECT * FROM hashtag_table ")
	for row in cursor:
		hashtag_edges.append(row)
	return hashtag_edges


def createHashtagGraph():
	supporters_hashtags=['coronavirus','CoronaVaccine','COVIDSecondWave','COVID19','SocialDistancing','MaskUp']
	deniers_hashtags=['Antilockdown','antivaxxers','KBF','Antilockdownprotest','antimask','BellsPalsy','plandemic']

	list_of_edges=getHashTagGraphEdges()

	G=nx.Graph()

	#get only the edges with weight!=0
	weighted_edges=[]
	all_nodes=[]
	for edge in list_of_edges:
		if(edge[2]!=0):
			temp_tup=(edge[0],edge[1])
			weighted_edges.append(temp_tup)
			all_nodes.append(edge[0])
			all_nodes.append(edge[1])

	G.add_edges_from(weighted_edges)

	for i,v in enumerate(all_nodes):
		if(v in supporters_hashtags):
			G.nodes[v]['color']='blue'
			G.nodes[v]['node_value']=1
		else:
			G.nodes[v]['color']='red'
			G.nodes[v]['node_value']=-1

	nx.write_gexf(G, "hashtag_graph.gexf")




createHashtagGraph()
