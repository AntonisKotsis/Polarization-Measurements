import networkx as nx

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#

#THIS SCRIPT CALCULATES THE 
#PERCENTAGE OF THE NODES THAT ARE CONNECTED 
#ONLY WITH NODES OF THE SAME COLOR 
#WE USE THAT AS ANOTHER MEASUREMENT OF CONTROVERSY EXISTENCE IN THE GRAPH
#THE NUMBER WE GET AS A RESULT BELONGS TO THE RANGE OF [0,1] 
#THE CLOSER THIS NUMBER IS TO 1 THE MORE CONTROVERSIAL THE GRAPH IS CONCIDERED

#=========================================================#

graph_name=input ("Enter graph name:")
G=nx.read_gexf(graph_name)


same_connected=0
different_connected=0
for g in G:
	last_color=''
	breaker=False
	neigh_list=list(G.neighbors(str(g)))
	last_color=G.nodes[str(g)]['color']

	#check the colors of the neighbors 
	#only if there are 2 or more neighbors for the current node g

	if(len(neigh_list)>=2):
		for neighbor in neigh_list:
			if(G.nodes[str(neighbor)]['color']==last_color):
				continue
			else:
				breaker=True
				break

		if(breaker):
			
			different_connected+=1
		else:
			same_connected+=1


x=same_connected/(same_connected+different_connected)
print(round(x,3))