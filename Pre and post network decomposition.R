
#############################################################################
##### The code below divides the following connections into the different kinds where there
#is a before network labelled 'pre' and an after network labeled 'post'
#############################################################################

library('igraph') #The following use the R igraph package

#############################################################################
#1. Extracts the completely new unreciprocated connections
#############################################################################

#deletes the connections in the post event network that are reciprocal
postunrec<-delete.edges(post, which(is.mutual(post, es = E(post))=="TRUE"))

#selects the unreciprocated connections that were not in the pre event network i.e. the new ones
newunrec<-graph.difference(postunrec,pre)


#############################################################################
#2. Extracts the completely new reciprocated connections
#############################################################################

#The next two commands creates a new network that is the difference between the post and pre network and obtains the edges
#b contains edges that are in the post network, but which are not in the pre network
b<-graph.difference(post,pre)

#Only select new connections that are completely reciprocal
newrec<-delete.edges(b, which(is.mutual(b)=="FALSE)

#The below calculates the edges that were in the network before the event, but which have since disappeared
#This is not used further, but is included for completeness
edgesgone<-graph.difference(pre, post)


############################################################################
#3. Extracts the new connections that consolidating an existing connection creating a reciprocal connection
#  Labelled newold
############################################################################

#Deletes the edges of the post event graph that are not reciprocal, to leave the post event reciprocal connections
postrec<-delete.edges(post, which(is.mutual(post, es = E(post))=="FALSE"))

#Extracts the reciprocal connections that are were formed by consolidation of an existing connection
newreccon<-graph.difference(postrec, newrec)

#Extracts the edges in the consolidated reciprocal connections that are new i.e. the new connections that created the reciprocal connection
newoldint<-graph.difference(newreccon, pre)


###########################################################################
#4. Extracts the connections that are in both the pre and post networks
# Labelled preandpost

preandpost<-graph.intersection(post, pre)

###########################################################################
#Checks that everything sums together
#Connections in the post network =1. New unreciprocated connections (newunrec) + 2. New reciprocal connections (newrec) +3. New consolisated connections (newold) + 4. Connections from the pre network that are in the post network

#Sticks all the connections back together
testgraph<-graph.union(newunrec, newrec, newold, preandpost)

#Checks that it is the same graph
graph.difference(post, testgraph) #should be 0




