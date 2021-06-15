from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import text
import random
import sqlite3

#				Author:Mitos-Kotsis Antonios		     #
#						cs3028@uoi.gr 					 #
#========================================================#
#In this script I implemented a classification algorithm
#Trained the NLP using 2,000 tweets from the database
#After that I used the testing set and picked  tweets in order to test the results
#Finally the accuracy of the NLP was calculated

def print_top_words(corpus,n):

	for c in range(n):
		print(corpus[c][0],"---->",corpus[c][1],"   ",corpus[c][1]/len(corpus))
	print("\n")

#Function that calculates most popular terms in tweets
def show_top_words(corpus,n=None):
	preprocess_terms=["https","amp","new","people","cases","19"]
	preprocess_terms.extend(["#coronavirus","#CoronaVaccine","#COVIDSecondWave","#COVID19","#SocialDistancing","#MaskUp"])
	preprocess_terms.extend(["#Antilockdown","#antivaxxers","#KBF","#Antilockdownprotest","#antimask","#BellsPalsy","#plandemic"])
	stop_words=text.ENGLISH_STOP_WORDS.union(preprocess_terms)
	vec=CountVectorizer(stop_words=stop_words).fit(corpus)
	bag_of_words=vec.transform(corpus)
	sum_words=bag_of_words.sum(axis=0)
	words_freq=[(word, sum_words[0, idx]) for word, idx in     vec.vocabulary_.items()]
	words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
	return words_freq[:n]


data=[]
data_labels=[]

#Following we define two corpus one for each team
#We made this in order to find out which words each team uses more
corp=[]
supp_corp=[]
den_corp=[]
db_connection=sqlite3.connect('tweet.db')
cursor=db_connection.cursor()

db_rows=cursor.execute("SELECT * FROM coronavirus_table")
counter=0
redC=0
blueC=0
for row in db_rows:
	if(counter>2000):
		break
	if(row[6]!=None and row[4]!=None):
		data.append(row[6])
		corp.append(row[6])

		data_labels.append(row[4])
		#print("data",row[6])
	if(row[4]=='Red'):
		redC+=1
		if(row[6]!=None):
			den_corp.append(row[6])

	else:
		blueC+=1
		if(row[6]!=None):
			supp_corp.append(row[6])

	counter+=1


print("red:",redC)
print("blues:",blueC)

#Transform the tweets to vectors

vectorizer= CountVectorizer(
	analyzer='word',
	lowercase=False
)

features=vectorizer.fit_transform(data)

features_nd=features.toarray()

#train the NLP

X_train , X_test , y_train , y_test=train_test_split(
	features_nd,
	data_labels,
	train_size=0.10,
	random_state=1234
)


log_model=LogisticRegression()

log_model=log_model.fit(X=X_train,y=y_train)
y_pred=log_model.predict(X_test)

j=random.randint(0,len(X_test)-10)

#test the results of the NLP
#Must do for all items in database (polu xrono )
for i in range (j,j+10):
	print(y_pred[i])
	ind=features_nd.tolist().index(X_test[i].tolist())
	print(data[ind].strip())
	print("\n"+"\n")

#calculate accuracy score of the NLP
#the accuracy should be >= 85% in order the NLP to be considered accurate
print(accuracy_score(y_test,y_pred))

#print(show_top_words(corp,5))
#print(show_top_words(den_corp,10))
#print(show_top_words(supp_corp,10))
den_corp=show_top_words(den_corp,None)
supp_corp=show_top_words(supp_corp,None)
print("Deniers")
print_top_words(den_corp,5)
print("Supporters")
print_top_words(supp_corp,5)
