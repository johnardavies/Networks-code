from tweet_auth import *  #Imports twitter keys and access tokens
####################imports various modules to make things work###########################################
from twython import Twython
import json
import csv
import time
import codecs
from collections import defaultdict
###########################################################################################################
#Programme which gets the userinfo from a set of Twitter screen_names 100 at a time
###########################################################################################################
###########################################################################################################

###########################################################################################################
# 1. Writes the userinfo data to a csv
def write(x):
 p = open('out filepath.txt', "a")
#Create a dictionary to store the data
 for entry in x: #Go through the entries in the returned json and extract the data and writes it as a csv
     ids = entry['id']
     screen_name = entry['screen_name'].encode('utf-8')
     friends=entry['friends_count']
     followers=entry['followers_count']
     location=entry['location'].encode('utf-8')
     location=location.replace(",","") #removes the commas as they will throw the formatting
     url=entry['url']
     description=entry['description'].encode('utf-8')
     description=description.replace(",","") #remloves the commas as they will throw the formatting
     #removes the full stop as it seems to raise issues
     description=description.strip()#''\t\n\r')#removes any extra whitespace as this seemed to be messing it up
     description=description.replace("\n"," ").replace("\r"," ") #Removes any remaining new lines and carriage returns
     p.write(str(ids)+','+str(screen_name)+','+str(friends)+','+str(followers)+','+str(location)+','+str(url)+','+str(description)+'\n')
 p.close()  


##########################################################################################################
#2.Reads the userid info in from the csv file and fills up a list called
#stored to take them

stored=[]

ifile  = open('csv infile path.csv', "rb")
field_names=['ids']
reader =  csv.DictReader(ifile,fieldnames=field_names) #T
print reader
#creates a dictionary with the ids as the keys and the names and speaker status as the values
names=defaultdict(list)
for row in reader:
    row['ids']=row['ids'].replace("\n","").replace('\r', '')
    stored.append(row['ids'])
print stored



#Creates a Twitter client
twitter = Twython(APP_KEY,APP_SECRET, access_token=ACCESS_TOKEN)

#######################################################################################################################################
#3.The part of the programme that queries the Twitter API up to 100 Twitter ids at a time###############################################

for i in range(0, len(stored)):
    if ((i%99)==0) & (i>0):   #The count has reached 100, in which case the details can be passed to the lookup API call
      b=int(i-99)
      print b, i
      print '100'
      green=twitter.lookup_user(screen_name=stored[b:i])
      write(green)
      #store.append(green)
      time.sleep(1)
    elif i==(len(stored)-1):  #The count has reached the end of the list, but not 100. In which case feed the remaining items to the lookup API call
      print 'under 100'
      f=int(i-i%99)
      print f, i+1
      green=twitter.lookup_user(screen_name=stored[f:i+1])
      write(green)
    else:
      pass    


 







