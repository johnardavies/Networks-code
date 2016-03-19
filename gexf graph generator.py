import csv
from collections import defaultdict
import json
import os

###########################################################################################################
#This takes information on who a group of people follow and their Twitter profile information
#and merges it into a gexf graph file format that can be read by gephi
###########################################################################################################

def graphwrite(x):
############################################################################################################
#reads in the dictionary created from the querying the api as a file #######################################
############################################################################################################
 json_data=open(x)
 type(json_data)
 #parses the json
 data =json.load(json_data)
 #The next section changes the code away from unicode to sort out the matching
 #otherwise all the keys start with'u
 for key1 in data.keys():
     key2=key1.encode('utf-8')
     data[key2]=data.pop(key1)

##############################################################################################################
#1. Reads in the node information and turns it into a dictionary##########################################
##############################################################################################################
 ifile  = open('infile path of Twitter profile information'.csv', "rb")
 field_names=['ids', 'screen_name', 'friends_count', 'followers_count', 'location', 'url']
 reader =  csv.DictReader(ifile,fieldnames=field_names) 
#creates a dictionary with the ids as the keys and the Twitter profile information as the values
 names=defaultdict(list)
 for row in reader:
   names[str(row['ids'])].append(str(row['screen_name']))
   names[str(row['ids'])].append(str(row['friends_count']))
   names[str(row['ids'])].append(str(row['followers_count']))
   names[str(row['ids'])].append(str(row['location']))
   names[str(row['ids'])].append(str(row['url']))

#############################################################################################################
#2. switches the keys of the dictionary data from being user names to user ids
#as the data was collected using user names not screen names.
#############################################################################################################
 #####Loops through the keys of the data which are user names
 for key2 in data.keys():
  #Loops through the keys of the names data which are user names
    for key3 in names:
     # if the username which is the key matches the user name in the dictionary
       if (names[key3][0]==str(key2)):
        #  swap the user name with the userid so that the keys of data are the userid
          data[key3]=data.pop(key2)

#Prints what the keys are as a visual check
 print(data.keys())
############################################################################################################# 
#3.creates the edge data for the graph#######################################################################
#############################################################################################################
 store2=defaultdict(list)
 for key1 in data:#loops through the keys
  for val in data[key1]: #takes the values from each of the keys
   for key2 in data:     #loops through all of the keys
     if (str(val)==str(key2)):  #if a value is equal i.e. that person is in the list of people we are studying add it to our inside the event list
       store2[str(key1)].append(val)
############################################################################################################
#4.Starts the graph generation##############################################################################
## sets up a file that the graph will be written to based on the basename of the file
 path=os.path.join("outfile path",os.path.basename(x)) 
 p = open(path, "a")

#adds in the standard graph headers
 p.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
 p.write('<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">'+'\n')
 p.write('<graph  mode="dynamic" defaultedgetype="directed" timeformat="date">'+'\n')

 p.write('<attributes class="node" mode="static">'+'\n')
 p.write('<attribute id="1" title="screen_name" type="string"/>'+'\n')
 p.write('<attribute id="2" title="friends_count" type="string"/>'+'\n')
 p.write('<attribute id="3" title="followers_count" type="string"/>'+'\n')
 p.write('<attribute id="4" title="location" type="string"/>'+'\n')
 p.write('<attribute id="5" title="url" type="string">'+'\n')
 p.write('</attribute>' +'\n')  
 p.write('</attributes>'+'\n')    
 

 p.write('<nodes>'+'\n')
#create a vector of unique ids
#writes the nodes for the twitter graph######################################################
 for key in names:
   p.write('<node id="'+str(key)+'"'+' label="'+str(key)+'">'+'\n')
   p.write('<attvalues>'+'\n')
   p.write('<attvalue for ="1"' + ' value="'+str(names[key][0])+'"/>'+'\n')
   p.write('<attvalue for ="2"' + ' value="'+str(names[key][1])+'"/>'+'\n')
   p.write('<attvalue for ="3"' + ' value="'+str(names[key][2])+'"/>'+'\n')
   loc=str(names[key][3])
   loc=loc.replace('&' , "and") #swaps & for and as this can cause problems
   p.write('<attvalue for ="4"' + ' value="'+loc+'"/>'+'\n')
   desco=str(names[key][4])
   desco=desco.replace('&' , "and")
   p.write('<attvalue for ="5"' + ' value="'+desco+'"/>'+'\n')
   p.write('</attvalues>'+'\n')
   p.write('</node>'+'\n')
 p.write('</nodes>'+'\n')

   
 p = open(path, "a")
 a=0 #variables that indexes the edges set to 0
#Writes the edges for the twitter graph########################################################
 p.write('<edges>'+'\n')

 for key in store2:
   for val in store2[str(key)]:
    a=a+1
    p.write('<edge id="'+str(a)+'" source="'+ str(key)+'"' +' target="'+str(val)+'"/>'+'\n')
 p = open(path, "a")
 p.write('</edges>'+'\n')
 p.write('</graph>'+'\n')
 p.write('</gexf>'+'\n')
 p.close()

#################################################################################################
#################################################################################################
#The program reads the files in files in 1 by 1 and write them to a graph file
def main():

#The files below are the files that are going to be processed into graphs
#The files are in a python dictionay format (in json) with the screen_name as the key and the values
#the userids of the people they follow on Twitter
 files=['infile path for the connections information.json']

#Loops through the files and pulls them into the graphwriting programe
 for file in files:
    graphwrite(file)
 
#Note need to convert the .json to .gexf and switch the Label column to screen name in Gephi
        

