import json

#merges the two dictionaries that are in json format
def merge(x, y):
 #parses the json
 dat1=open(x)
 dat2=open(y)
 data1 =json.load(dat1)
 data2 =json.load(dat2)
 z = data1.copy()
 z.update(data2)
 return z


#Reads in the two datasers

fir='filepath1.json'

rem='filepath2.json'


#applies the function to them and writes the dictionary as a json file to the computer           
with open('outfilepath', 'w') as f:
    json.dump(merge(fir,rem), f)
