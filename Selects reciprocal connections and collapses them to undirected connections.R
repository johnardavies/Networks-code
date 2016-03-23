library('igraph')

#Reads in a directed graph file selects only the reciprocal connections, collapses the reciprocal
#edges to a single edge and then outputs it
graphin<-read.graph("infilepath.graphml", format="graphml")

#selects only the reciprocal connections
graphrec<-delete.edges(graphin, which(is.mutual(graphin)=="FALSE"))

#collapses the reciprocal edges to undirected single edges
ungraphrec<-as.undirected(graphrec, mode = c("collapse"))

#Writes the networks back to the disk
write.graph(ungraphrec,"outfilepath.graphml",format=c("graphml") ) 
