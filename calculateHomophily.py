import networkx as nx
import os

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#

#THIS SCRIPT CALCULATES THE 
#HOMOPHILY OF THE GRAPH
#WE USE THAT AS ANOTHER MEASUREMENT OF CONTROVERSY EXISTENCE IN THE GRAPH
#THE NUMBER WE GET AS A RESULT BELONGS TO THE RANGE OF 0..1 
#THE CLOSER THIS NUMBER IS TO 1 THE MORE CONTROVERSIAL THE GRAPH IS CONCIDERED

#=========================================================#

def findCovidHomophily():
	graph_name=input ("Enter graph name:")
	G=nx.read_gexf(graph_name)

	total_homophily=0
	total_nodes=0
	different_connected=0
	for g in G:
		same_connected=0
		node_homophily=0
		node_color=''
		neigh_list=list(G.neighbors(str(g)))
		node_color=G.nodes[str(g)]['color']
	
		
		for neighbor in neigh_list:
				if(G.nodes[str(neighbor)]['color']==node_color):
					same_connected+=1
				#total_nodes+=1
	
		node_homophily=same_connected/len(neigh_list)
	
		total_homophily+=node_homophily
		total_nodes+=1
	
	print("Covid Homophily:",total_homophily/total_nodes)
	print("Total nodes:",total_nodes)


#Create a suitable graph file for the 
#reference hashtags of aalto university
def createGraphFile(filename):
	
	edges=open("retweet_graph_"+filename+"_threshold_largest_CC.txt","r")
	
	edges_list=[]
	out_file=open(filename+"_out.txt",'w')
	last_user=''

	graph_list=[]
	neigh_list=[]


	
	for edge in edges:
		edge=edge.strip()
		edges_list.append(edge.split(','))

	last_user=edges_list[0][0]

	for e in edges_list:
		if(e[0]==last_user):
			neigh_list.append(e[1])
		else:
			graph_list.append((last_user,neigh_list))
			out_list=[]
			out_list.append(last_user)
			for n in neigh_list:
				out_list.append(n)
			for o in out_list:
				out_file.write(o+',')
			
			out_file.write('\n')
			last_user=e[0]

			neigh_list.clear()
			neigh_list.append(e[1])

#Find the Homophily for
#-Beefban
#-Russia March
#-InternationalKissingDay
#-Ultralive



def findHomophily(filename):
	comm1=open("community1_"+filename+".txt","r")
	comm2=open("community2_"+filename+".txt","r")
	comm1_list=[]
	comm2_list=[]

	graph_file=open(filename+"_out.txt")
	graph=[]

	total_homophily=0

	for c in comm1:
		comm1_list.append(c.strip())

	for c in comm2:
		comm2_list.append(c.strip())


	for g in graph_file:
		g=g.strip()
		g=g[:-1]
		graph.append(g.split(','))

	total_nodes=len(comm1_list)+len(comm2_list)
	sample_size=0
	for g in graph:
		#print(g[0])
		neig_len=len(g)-1
		source_comm=-1
		dest_comm=-2
		same_connected=0
		node_homophily=0
		#find the community that source belongs to
		if(g[0] in comm1_list):
			source_comm=1
		else:
			source_comm=2

		#access the neighbours
		for i in range(1,len(g)):
			if(g[i] in comm1_list):
				dest_comm=1
			elif(g[i] in comm2_list):
				dest_comm=2
			else:
				print("community not found")

			if(source_comm==dest_comm):
				same_connected+=1
		sample_size+=neig_len
		node_homophily=same_connected/neig_len
		total_homophily+=node_homophily
	print(filename, "Homophily:",total_homophily/total_nodes)
	#print(sample_size,total_nodes)

createGraphFile("beefban")
findHomophily("beefban")

createGraphFile("ultralive")
findHomophily("ultralive")

createGraphFile("russia_march")
findHomophily("russia_march")

createGraphFile("germanwings")
findHomophily("germanwings")

createGraphFile("nationalkissingday")
findHomophily("nationalkissingday")

findCovidHomophily()