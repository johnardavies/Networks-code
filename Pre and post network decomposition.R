
##################################################################################################
##### The code below divides the following connections into the different kinds where there
#is a before network labelled 'pre' and an after network labeled 'post'


library("igraph") #The following use the R igraph package


#############################################################################
#1. Extracts the new unreciprocated connections
#Labelled newunrec
#############################################################################

#The next command creates a new network that is the difference between the post and pre network and obtains the edges
#b contains edges that are in the post network, but which are not in the pre network
b<-graph.difference(post,pre, byname=FALSE)

###################################################################################################
#The graph comparisons here are done on the vertex ids. This depends on the number of vertices remaining unchanging
#if byname is set to true then the comparison is done by name; this requires the vertices to have name attributes
###################################################################################################

#Calculates the post event network of reciprocal connections
postrec<-delete.edges(post, which(is.mutual(post)=="FALSE"))

#selects the new connections that were not completely new reciprocal i.e. the new unreciprocated ones or 
#the ones consolidating an existing connection
newunrec1<-delete.edges(b, which(is.mutual(b)=="TRUE"))

newunrec<-graph.difference(newunrec1, postrec, byname=FALSE)


#############################################################################
#2. Extracts the completely new reciprocated connections
# Labelled newrec
#############################################################################

#Only select new connections that are completely reciprocal
newrec<-delete.edges(b, which(is.mutual(b)=="FALSE"))

#The below calculates the edges that were in the network before the event, but which have since disappeared
#This is not used further, but is included for completeness
edgesgone<-graph.difference(pre, post, byname=FALSE)


############################################################################
#3. Extracts the new connections that consolidating an existing connection creating a reciprocal connection
#  Labelled newold
############################################################################

#Extracts the reciprocal connections that were formed by consolidation of an existing connection
newreccon<-graph.difference(postrec, newrec, byname=FALSE)

#Extracts the edges in the consolidated reciprocal connections that are new i.e. the new connections that created the reciprocal connection
newold<-graph.difference(newreccon, pre, byname=FALSE)


###########################################################################
#4. Extracts the connections that are in both the pre and post networks i.e. that stayed the same
# Labelled preandpost 
###########################################################################
preandpost<-graph.intersection(post, pre, byname=FALSE)

###########################################################################
#Checks that everything sums together
#Connections in the post network =1. New unreciprocated connections (newunrec) + 2. New reciprocal connections (newrec) +3. New consolisated connections (newold) + 4. Connections from the pre network that are in the post network (preandpost)

#Sticks all the connections back together
testgraph<-graph.union(newunrec, newrec, newold, preandpost, byname=FALSE)

ecount(post)-ecount(testgraph) #should be 0

#Checks that it is the same graph should be no difference. The edges should be the same
graph.difference(post, testgraph, byname=FALSE)
##########################################################################



