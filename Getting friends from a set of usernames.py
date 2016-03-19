from tweet_auth import *  #Imports my twitter keys and access tokens
####################imports various modules to make things work###########################################
#imports twython and json
from twython import Twython
import json
import csv
import time
from collections import defaultdict

############################################################################################################
#This programme reads a csv of a set of screen names and
#returns a json dictionary of the user ids of the people they follow

#creates a twitter client
twitter = Twython(APP_KEY,APP_SECRET, access_token=ACCESS_TOKEN)

#creates the dictionary the results will be stored in
stored=defaultdict(list)

#Reads in the csv with the Twitter handles
ifile  = open('inpath.csv', "rb")

for name in ifile:
  next_cursor=-1 #initiates the cursor 
  try: 
    while(next_cursor != 0):#keeps looping through as long as there are pages there    
             print(name)
             time.sleep(60)  # sets a time delay of 60 seconds to keep within the rate limits
             #gets the people followed by the screen name
             following=twitter.get_friends_ids(screen_name=str(name), cursor=next_cursor)
             for x in following[u'ids']:  #loops through the ids returned by the Twitter api
                name=name.encode('utf-8')
                stored[str(name)].append(x)  # and appends them to the dictionary where the key is the associated persons user id
             next_cursor=following['next_cursor']  #gets the next cursor value
  except:  # if the call fails which may be because there are no more pages
      print('unable to access the people followed by '+str(name)+','+str(next_cursor)+'\n')  
#writes the dictionary as a json file to the computer           
with open('outpath.json', 'w') as f:
    json.dump(stored, f)





     



