import fileinput
import re
import csv
from collections import defaultdict

########Reads in the a csv with 1. The name of the person tweeting  2. Their retweet##########################
#From this it reconstructs the social network in terms of retweets and mentions and writes this as an edgelist
##############################################################################################################
ifile  = open('infilepath.csv', "rb")
#The infile has a column called 'Author' which is the person that tweeted and a column called 'Text' which is the
#content of the tweet
reader =  csv.DictReader(ifile)#

filepath='outfilepath.csv'
#This is the filepath that the edge list is written to

#creates a dictionary with the ids as the keys and the names and speaker status as the values
names=defaultdict(list)
for row in reader:
#Regex by Shamir Javaid
#(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)
#The first bit of the regex is to avoid matching emails e.g. johndoe@hotmail.com
#?<=^ #Matches if the string is proceeded by an empty string proceeding the start  e.g.m = re.search('(?<=^)def', 'def') matches def, but not m = re.search('(?<=^)def', 'abcdef')
#(?<=[^a-zA-Z0-9-_\.]) # [^a-zA-Z0-9-_\.] means do not match alphanumeric characters before the @
#[A-Za-z]+[A-Za-z0-9]+ #This catches the start of the Twitter handle which must be a letter[A-Za-z] and then allows
#for the possibilities of numbers appearing later on with[A-Za-z0-9]   
     try:
      #All retweets are prefixed by an RT
      rtest = re.match(r'^RT', row['Text']).group(0)
      #If it's a retweet extracts the first names after the RT which is that of the person who has been retweeted
      searchObj1 = re.search(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', row['Text']).group() #Note as stands cuts Twitter handles with a _ in them 
      searchObj1=searchObj1.replace("@", "") #Removes the @
      with open(filepath, "a",) as csvFile: #Writes the data to a csv 
        writer=csv.writer(csvFile, lineterminator='\n')
        writer.writerow((str(row['Author']),str(searchObj1),'retweet')) #Writes an edge and labels it as a retweet
      csvFile.close()  
     except:
      try:
       #if it's a mention extracts all the names of the people mentioned in the tweet
       searchObj = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', row['Text'])
       for x in searchObj: #Loops through the other people mentioned in the tweet and generates separate edges for each
        with open(filepath, "a",) as csvFile: #Writes the data to a csv file
         writer=csv.writer(csvFile, lineterminator='\n')
         writer.writerow((str(row['Author']),str(x),'mention')) #Writes an edge and labels it as a mention
        csvFile.close()  
      except:
       print 'parsing failed'

#Note maybe runs a bit slow

