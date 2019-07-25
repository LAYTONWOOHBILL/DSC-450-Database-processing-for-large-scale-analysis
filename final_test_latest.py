# -*- coding: utf-8 -*-
"""Final_test_Latest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lHXOLp8ViB8fQWsAp9zb8srKWrq2B7_W

### 1

a.	Create a 3rd table incorporating the Geo table (in addition to tweet and user tables that you already have from HW4 and HW5) and extend your schema accordingly. You do not need to use ALTER TABLE, it is sufficient to just re-make your schema.
You will need to generate an ID for the Geo table primary key (you may use any value or reasonable combination of values as long as it is unique) for that table and link it to the Tweet table (foreign key should be in the Tweet). In addition to the primary key column, the geo table should have at least the “type”, “longitude” and “latitude” columns.
"""

import sqlite3
conn = sqlite3.connect('dsc450_Final_web.db')
c = conn.cursor()
                       
usertable = '''CREATE TABLE user_id(
    id         int,
    name       text,
    screen_name  text,
    description  text,
    friends_count  int,
    
    PRIMARY KEY (id)
);'''

geotable = '''CREATE TABLE geo(
    id int,
    type text,
    longitude text,
    latitude text,
    
    PRIMARY KEY (id)
);'''

tweettable = '''CREATE TABLE tweet(
    id_str  int,
    created_at text,
    text  text,
    source  text, 
    in_reply_to_user_id int,
    in_reply_to_screen_name  text,
    in_reply_to_status_id int,
    retweet_count int,
    contributors  text,
    geo_id text,
    user_id  int,
    
    CONSTRAINT Tweets_PK  PRIMARY KEY (id_str),

    CONSTRAINT Tweets_FK1 FOREIGN KEY (user_id)
    REFERENCES User(id),
    
    CONSTRAINT Tweets_FK2 FOREIGN KEY (geo_id)
    REFERENCES geo(id)
);'''

    
try:
    c.execute('drop table tweet')
    c.execute('drop table user_id')
    c.execute('drop table geo')
except:
    pass

import sys
import json
import urllib
import time

c.execute(usertable)
c.execute(geotable)
c.execute(tweettable)

startweb = time.time()
webFD=urllib.request.urlopen ("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
d = open('OneDayOfTweets1.txt','w')

user_list, tweet_list, geo_list = [], [], [] 
geoid = 0

for i in range(1000000):
    alltweet=webFD.readline()
    d.write(alltweet.decode('utf8'))
    try:
        tweet = alltweet
        tdict = json.loads(tweet)
    except:
        pass
    else:
        newRowUser = [] # hold individual values of to-be-inserted row for user table
        userKeys = ['id', 'name', 'screen_name', 'description', 'friends_count']
        userDict = tdict['user']
        for key in userKeys: # For each dictionary key we want
            if userDict[key] == 'null' or userDict[key] == '':
                newRowUser.append(None)   # proper NULL
            else:
                newRowUser.append(userDict[key]) # use value as-is
        user_list.append((newRowUser))
            
    
        newRowTweet = [] # hold individual values of to-be-inserted row
        tweetKeys = ['id_str','created_at','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors']
        geoid += 1
        for key in tweetKeys:
            if tdict[key] == 'null' or tdict[key] == '':
                newRowTweet.append(None)   # proper NULL
            else:
                newRowTweet.append(tdict[key]) # use value as-is
        userDict = tdict['user'] # This the the dictionary for user information
        if tdict['geo']:
            newRowTweet.append(geoid) # Take the point type
            geo_list.append((geoid,tdict['geo']['type'],tdict['geo']['coordinates'][0],tdict['geo']['coordinates'][1]))
        else:
            newRowTweet.append(None)
        newRowTweet.append(userDict['id']) # User id/ foreign key
        tweet_list.append((newRowTweet))
        
d.close()

stopweb = time.time()
print("diff "+str(stopweb-startweb))
startinsert = time.time()
c.executemany('INSERT OR IGNORE INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)',tweet_list) 
c.executemany('INSERT OR IGNORE INTO user_id VALUES(?,?,?,?,?)',user_list)
c.executemany('INSERT OR IGNORE INTO geo VALUES(?,?,?,?)',geo_list)
stopinsert = time.time()
print("diff "+str(stopinsert-startinsert))

"""b.	Use python to download from the web and save to a local text file (not into database yet, just to text file) at least 1,000,000 lines worth of tweets. Test your code with fewer rows first and only time it when you know it works. Report how long did it take.

NOTE: Do not call read() or readlines() without any parameters at any point. That command will attempt to read the entire file which is too much data.

c.	Repeat what you did in part-b, but instead of saving tweets to the file, populate the 3-table schema that you created in SQLite. Be sure to execute commit and verify that the data has been successfully loaded (report loaded row counts for each of the 3 tables).
How long did this step take?
"""

start = time.time()
print(c.execute('select count(*) from user_id').fetchall())
print(c.execute('select count(*) from tweet').fetchall())
print(c.execute('select count(*) from geo').fetchall())
print(c.execute('select count(*) from tweet where geo_id != "None"').fetchall())
print(c.execute('select count(*) from tweet where geo_id is NULL').fetchall())
stop = time.time()
print("diff "+str(stop-start))

"""d.	Use your locally saved tweet file (created in part-b) to repeat the database population step from part-c. That is, load 1,000,000 tweets into the 3-table database using your saved file with tweets (do not use the URL to read twitter data). 
How does the runtime compare with part-c?
"""

import sqlite3
import json
import time


confile = sqlite3.connect('dsc450_Final_file2.db')
cfile= confile.cursor()
                       
usertable = '''CREATE TABLE user_id(
    id         int,
    name       text,
    screen_name  text,
    description  text,
    friends_count  int,
    
    PRIMARY KEY (id)
);'''

geotable = '''CREATE TABLE geo(
    id int,
    type text,
    longitude text,
    latitude text,
    
    PRIMARY KEY (id)
);'''

tweettable = '''CREATE TABLE tweet(
    id_str  int,
    created_at text,
    text  text,
    source  text, 
    in_reply_to_user_id int,
    in_reply_to_screen_name  text,
    in_reply_to_status_id int,
    retweet_count int,
    contributors  text,
    geo_id text,
    user_id  int,
    
    CONSTRAINT Tweets_PK  PRIMARY KEY (id_str),

    CONSTRAINT Tweets_FK1 FOREIGN KEY (user_id)
    REFERENCES User(id),
    
    CONSTRAINT Tweets_FK2 FOREIGN KEY (geo_id)
    REFERENCES geo(id)
);'''

try:
    cfile.execute('drop table tweet')
    cfile.execute('drop table user_id')
    cfile.execute('drop table geo')
except:
    pass

cfile.execute(tweettable)
cfile.execute(usertable)
cfile.execute(geotable)

startfile = time.time()
file = open('OneDayOfTweets1.txt','r')
user_list_file, tweet_list_file, geo_list_file = [], [], [] 
geoid_infile = 0


for i in range(1000000):
    alltweets=file.readline()
    try:
        tweets = alltweets
        tdict = json.loads(tweets)
  
    except:
        pass
    else:
        newRowUser = [] # hold individual values of to-be-inserted row for user table
        userKeys = ['id', 'name', 'screen_name', 'description', 'friends_count']
        userDict = tdict['user']
        for key in userKeys: # For each dictionary key we want
            if userDict[key] == 'null' or userDict[key] == '':
                newRowUser.append(None)   # proper NULL
            else:
                newRowUser.append(userDict[key]) # use value as-is
        user_list_file.append((newRowUser))
            
    
        newRowTweet = [] # hold individual values of to-be-inserted row
        tweetKeys = ['id_str','created_at','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors']
        geoid_infile += 1
        for key in tweetKeys:
            if tdict[key] == 'null' or tdict[key] == '':
                newRowTweet.append(None)   # proper NULL
            else:
                newRowTweet.append(tdict[key]) # use value as-is
        userDict = tdict['user'] # This the the dictionary for user information
        if tdict['geo']:
            newRowTweet.append(geoid_infile) # Take the point type
            geo_list_file.append((geoid_infile,tdict['geo']['type'],tdict['geo']['coordinates'][0],tdict['geo']['coordinates'][1]))
        else:
            newRowTweet.append(None)
        newRowTweet.append(userDict['id']) # User id/ foreign key
        tweet_list_file.append((newRowTweet))
        
file.close()
stopfile = time.time()
print("diff "+str(stopfile-startfile))
startfileinsert = time.time()
cfile.executemany('INSERT OR IGNORE  INTO user_id VALUES(?,?,?,?,?)',user_list_file)
cfile.executemany('INSERT OR IGNORE  INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)',tweet_list_file) 
cfile.executemany('INSERT OR IGNORE  INTO geo VALUES(?,?,?,?)',geo_list_file) 
stopfileinsert = time.time()
print("diff "+str(stopfileinsert-startfileinsert))

start = time.time()
print(cfile.execute('select count(*) from user_id').fetchall())
print(cfile.execute('select count(*) from tweet').fetchall())
print(cfile.execute('select count(*) from geo').fetchall())
print(cfile.execute('select count(*) from tweet where geo_id != "None"').fetchall())
print(cfile.execute('select count(*) from tweet where geo_id is NULL').fetchall())
stop = time.time()
print("diff "+str(stop-start))

"""e.	Re-run the previous step with a batching size of 1000 (i.e. by inserting 1000 rows at a time with executemany). 
How does the runtime compare when batching is used?
"""

conbatch = sqlite3.connect('dsc450_Final_batching.db')
cbatching= confile.cursor()
                       
usertable = '''CREATE TABLE user_id(
    id         int,
    name       text,
    screen_name  text,
    description  text,
    friends_count  int,
    
    PRIMARY KEY (id)
);'''

geotable = '''CREATE TABLE geo(
    id int,
    type text,
    longitude text,
    latitude text,
    
    PRIMARY KEY (id)
);'''

tweettable = '''CREATE TABLE tweet(
    id_str  int,
    created_at text,
    text  text,
    source  text, 
    in_reply_to_user_id int,
    in_reply_to_screen_name  text,
    in_reply_to_status_id int,
    retweet_count int,
    contributors  text,
    geo_id text,
    user_id  int,
    
    CONSTRAINT Tweets_PK  PRIMARY KEY (id_str),

    CONSTRAINT Tweets_FK1 FOREIGN KEY (user_id)
    REFERENCES User(id),
    
    CONSTRAINT Tweets_FK2 FOREIGN KEY (geo_id)
    REFERENCES geo(id)
);'''

try:
    cbatching.execute('drop table tweet')
    cbatching.execute('drop table user_id')
    cbatching.execute('drop table geo')
except:
    pass
import sys
import json
import urllib
import time

cbatching.execute(usertable)
cbatching.execute(geotable)
cbatching.execute(tweettable)

startweb = time.time()
webFD=urllib.request.urlopen ("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
user_list_b, tweet_list_b, geo_list_b = [], [], [] 
geoid_b = 0
loadCounter = 0

for i in range(1000000):
    alltweet=webFD.readline()
    if i % 1000 == 0: # Print a message every 100th tweet read
        print ("Processed " + str(i) + " tweets")
        
    try:
        tweet = alltweet
        tdict = json.loads(tweet)
        loadCounter = loadCounter + 1
    except:
        pass
    else:
        newRowUser = [] # hold individual values of to-be-inserted row for user table
        userKeys = ['id', 'name', 'screen_name', 'description', 'friends_count']
        userDict = tdict['user']
        for key in userKeys: # For each dictionary key we want
            if userDict[key] == 'null' or userDict[key] == '':
                newRowUser.append(None)   # proper NULL
            else:
                newRowUser.append(userDict[key]) # use value as-is
        if loadCounter < 1000: # Batching 50 at a time
            user_list.append((newRowUser))
        else:
            cbatching.executemany('INSERT OR IGNORE INTO user_id VALUES(?,?,?,?,?)',user_list)
            user_list_b = [] # Reset the list of batched tweets
    
            
        newRowTweet = [] # hold individual values of to-be-inserted row
        tweetKeys = ['id_str','created_at','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors']
        geoid_b += 1
        for key in tweetKeys:
            if tdict[key] == 'null' or tdict[key] == '':
                newRowTweet.append(None)   # proper NULL
            else:
                newRowTweet.append(tdict[key]) # use value as-is
        userDict = tdict['user'] # This the the dictionary for user information
        if tdict['geo']:
            newRowTweet.append(geoid) # Take the point type
            if loadCounter < 1000: # Batching 50 at a time
                geo_list_b.append((geoid,tdict['geo']['type'],tdict['geo']['coordinates'][0],tdict['geo']['coordinates'][1]))
        else:
            newRowTweet.append(None)
        newRowTweet.append(userDict['id']) # User id/ foreign key
        
        if loadCounter < 1000: # Batching 50 at a time
            tweet_list_b.append((newRowTweet))
        else:
            cbatching.executemany('INSERT OR IGNORE INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)',tweet_list_b)
            cbatching.executemany('INSERT OR IGNORE INTO geo VALUES(?,?,?,?)',geo_list_b)
            loadCounter = 0
            tweet_list_b = []
            geo_list_b = []# Reset the list of batched users
d.close()

stopweb = time.time()
print("diff "+str(stopweb-startweb))
startinsert = time.time()
cbatching.executemany('INSERT OR IGNORE INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)',tweet_list_b) 
cbatching.executemany('INSERT OR IGNORE INTO user_id VALUES(?,?,?,?,?)',user_list_b)
cbatching.executemany('INSERT OR IGNORE INTO geo VALUES(?,?,?,?)',geo_list_b)
stopinsert = time.time()
print("diff "+str(stopinsert-startinsert))

start = time.time()
print(cbatching.execute('select count(*) from user_id').fetchall())
print(cbatching.execute('select count(*) from tweet').fetchall())
print(cbatching.execute('select count(*) from geo').fetchall())
print(cbatching.execute('select count(*) from tweet where geo_id != "None"').fetchall())
print(cbatching.execute('select count(*) from tweet where geo_id is NULL').fetchall())
stop = time.time()
print("diff "+str(stop-start))

"""### 2

#### a.	Write and execute SQL queries to do the following. Don’t forget to report the running times in each part and the code you used

i.	Find tweets where tweet id_str contains “55” or “88” anywhere in the column
"""

start = time.time()
for i in cfile.execute('select * from tweet where id_str like "%55%" or  id_str like "%88%"').fetchall():
    print(i)
stop = time.time()
print("diff "+str(stop-start))

"""ii.	Find how many unique values are there in the “in_reply_to_user_id” column"""

start=time.time()
print(cfile.execute('''select count(*) from (
                        select distinct in_reply_to_user_id from tweet)''').fetchall())
stop = time.time()
print("diff "+str(stop-start))

"""iii.	Find the tweet(s) with the shortest, longest and average length text message."""

start=time.time()
for ltwe in cfile.execute('''select text from tweet 
                      where length(text) = (select min(length(text))from tweet)''').fetchall():
    print(ltwe)
    
print(cfile.execute('''select min(length(text))from tweet''').fetchall())
    
for stwe in cfile.execute('''select text from tweet 
                      where length(text) = (select max(length(text))from tweet)''').fetchall():
    print(stwe)

for avgtwe in cfile.execute('''select text from tweet 
                      where length(text) = (select round(avg(length(text)), -1) from tweet)''').fetchall():
    print(avgtwe)
stop = time.time()
print("diff "+str(stop-start))

"""iv.	Find the average longitude and latitude value for each user name."""

start = time.time()
for avgtwe in cfile.execute('''select user_id.name, geo.longitude, geo.latitude from tweet, geo, user_id
where geo.longitude = (select avg(longitude) from geo)and geo.latitude = (select avg(latitude) from geo) and tweet.geo_id = geo.id''').fetchall():
    print(avgtwe)
stop = time.time()
print("diff "+str(stop-start))

"""v.	Find how many known/unknown locations there were in total (e.g., 50,000 known, 950,000 unknown,  5% locations are available)"""

start = time.time()
a = cfile.execute('''select count(*)from tweet where geo_id is not null''').fetchall()
stop = time.time()
print(a)
print("diff "+str(stop-start))

start = time.time()
a=cfile.execute('''select count(*)from tweet where geo_id is not null''').fetchall()[0][0]/cfile.execute(
'''select count(*) from tweet''').fetchall()[0][0]
stop = time.time()
print('{0:.4f}%'.format((a* 100)))
print("diff "+str(stop-start))

"""vi.	Re-execute the query in part iv) 10 times and 100 times and measure the total runtime (just re-run the same exact query multiple times using a for-loop). Does the runtime scale linearly? (i.e., does it take 10X and 100X as much time?)"""

start1 = time.time()
for i in range(10):
    for avgtwe in cfile.execute('''select user_id.name, geo.longitude, geo.latitude from tweet, geo, user_id
where geo.longitude = (select avg(longitude) from geo)and geo.latitude = (select avg(latitude) from geo) and tweet.geo_id = geo.id''').fetchall():
        print(avgtwe)
stop1 = time.time()
print("diff "+str(stop1-start1))

start2 = time.time()
for i in range(100):
    for avgtwe in cfile.execute('''select user_id.name, geo.longitude, geo.latitude from tweet, geo, user_id
where geo.longitude = (select avg(longitude) from geo)and geo.latitude = (select avg(latitude) from geo) and tweet.geo_id = geo.id''').fetchall():
        print(avgtwe)
stop2 = time.time()
print("diff "+str(stop2-start2))

print("times "+str((stop2-start2)/(stop1-start1)))

"""#### b.	Write python code that is going to read the locally saved tweet data file from 1-b and perform the equivalent computation for parts 2-i and 2-ii only. How does the runtime compare to the SQL queries?"""

start = time.time()
openfile = open('OneDayOfTweets1.txt','r')
tweet_list = []
for i in range(1000000):
    alltweet=openfile.readline()
    try:
        tweet = alltweet
        tdict = json.loads(tweet)
    except:
        pass
    else:
        newRowTweet = [] # hold individual values of to-be-inserted row
        tweetKeys = ['id_str','created_at','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors']
        geoid += 1
        for key in tweetKeys:
            if tdict[key] == 'null' or tdict[key] == '':
                newRowTweet.append(None)   # proper NULL
            else:
                newRowTweet.append(tdict[key]) # use value as-is
        userDict = tdict['user'] # This the the dictionary for user information
        if tdict['geo']:
            newRowTweet.append(geoid) # Take the point type
        else:
            newRowTweet.append(None)
        newRowTweet.append(userDict['id']) # User id/ foreign key
        tweet_list.append((newRowTweet))

for x in range(len(tweet_list)):
    if '55' in tweet_list[x][0] or '88' in tweet_list[x][0]:
        print(tweet_list[x])
stop = time.time()
print("diff "+str(stop-start))

#print(cfile.execute('''select  in_reply_to_user_id from tweet''').fetchall())
#print(cfile.execute('''select * from (
#                       select distinct in_reply_to_user_id from tweet)''').fetchall())
#print(cfile.execute('''select count(*) from (
#                     select distinct in_reply_to_user_id from tweet)''').fetchall())
#print(cfile.execute('''select * from tweet
#                     where tweet.in_reply_to_user_id =93420016''').fetchall())
#
start = time.time()
openfile = open('OneDayOfTweets1.txt','r')
tweet_list = []
replylst=[]

for i in range(100000):
    alltweet=openfile.readline()
    try:
        tweet = alltweet
        tdict = json.loads(tweet)
    except:
        pass
    else:
        newRowTweet = [] # hold individual values of to-be-inserted row
        tweetKeys = ['id_str','created_at','text','source','in_reply_to_user_id', 'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 'contributors']
        geoid += 1
        for key in tweetKeys:
            if tdict[key] == 'null' or tdict[key] == '':
                newRowTweet.append(None)   # proper NULL
            else:
                newRowTweet.append(tdict[key]) # use value as-is
        userDict = tdict['user'] # This the the dictionary for user information
        if tdict['geo']:
            newRowTweet.append(geoid) # Take the point type
        else:
            newRowTweet.append(None)
        newRowTweet.append(userDict['id']) # User id/ foreign key
        tweet_list.append((newRowTweet))

for x in range(len(tweet_list)):
    if tweet_list[x][4] != None:
        if tweet_list[x][4] not in replylst:
            replylst.append(tweet_list[x][4])
withoutnone = len(replylst)
total= withoutnone +1  
print(total)

stop = time.time()
print("diff "+str(stop-start))

"""### 3.

a.	Export the contents of the User table from a SQLite table into a sequence of INSERT statements within a file. This is very similar to what you already did in Assignment 4. However, you have to add a unique ID column which has to be a string (you cannot use numbers). Hint: you can replace digits with letters, e.g., chr(ord('a')+1) gives you a 'b' and chr(ord('a')+2) returns a 'c'
"""

start = time.time()
def generateInsertStatements(table):
    data= c.execute('select * from '+ table).fetchall()
    d = open('inserts.txt','a') 
    a=0
    for value in data:
        a += 1
        unique_id = chr(ord('a')+100+a) 
        InsertStatements='INSERT INTO '+ table+' VALUES' + str((unique_id,) + (value)) +'\n'
        d.write(InsertStatements)
generateInsertStatements('user_id')
stop = time.time()
print("diff "+str(stop-start))
a = open("inserts.txt", 'r')# open file in read mode 
print("the file contains:") 
print(a.read())

"""b.	Create the same collection of INSERT for the User table by reading data from the local tweet file that you have saved earlier. 
How do these compare in runtime? Which method was faster?
"""

start = time.time()
def generateInsertStatementsfromtext(table):
    openfile = open('OneDayOfTweets1.txt','r')
    d = open('insertsfromtext.txt','a') 
    user_list = ()
    a=0
    for i in range(1000000):
        alltweet=openfile.readline()
        try:
            tweet = alltweet
            tdict = json.loads(tweet)
        except:
            pass
        else:
            newRowUser = () # hold individual values of to-be-inserted row for user table
            userKeys = ['id', 'name', 'screen_name', 'description', 'friends_count']
            userDict = tdict['user']
            for key in userKeys: # For each dictionary key we want
                if userDict[key] == 'null' or userDict[key] == '':
                    newRowUser += (None,)  # proper NULL
                else:
                    newRowUser +=(userDict[key],) # use value as-is
        a += 1
        unique_id = chr(ord('a')+100+a) 
        InsertStatements='INSERT INTO '+ table+' VALUES' + str((unique_id,) + (newRowUser)) +'\n'
        d.write(InsertStatements)
generateInsertStatementsfromtext('user_id')
stop = time.time()
print("diff "+str(stop-start))
a = open("insertsfromtext.txt", 'r')# open file in read mode 
print("the file contains:") 
print(a.read())

"""### 4. Export all three tables (Tweet, User and Geo tables) from the database into a |-separated text file (each value in a row should be separated by |). You do not generate SQL INSERT statements, just raw |-separated text data.

a.	For the Geo table, add a new column with relative distance from a fixed point which is the location of CDM (41.878668, -87.625555). You can simply treat it as a point-to-point Euclidean distance (although bonus points for finding a real distance in miles) and round the longitude and latitude columns to a maximum of 4 digits after the decimal.
"""

start= time.time()
f = open('geo.txt', 'w')
s = '|'
for row in cfile.execute('select * from geo').fetchall():
    a = row[0]
    b = row[1]
    c = float(row[2])
    d= float(row[3])
    diff = round(((41.878668-c)**2+(-87.625555-d)**2)**(1/2),4)
    f.write(str(a)+s+b+s+str(c)+s+str(d)+s+str(diff)+ '\n')
f.close()
stop = time.time()
print("diff "+str(stop-start))
a = open('geo.txt', 'r')
print("the file contains:") 
print(a.read())

"""b.	For the Tweet table, add two new columns from the User table (“name” and “screen_name”) in addition to existing columns."""

start= time.time()
f = open('tweet.txt', 'w')
for row in cfile.execute('select tweet.*, name, screen_name from tweet, user_id where tweet.user_id = user_id.id').fetchall():
    f.write(   str(row)[1:-1].replace(', ', '|')  + '\n' )
f.close()
stop = time.time()
print("diff "+str(stop-start))
a = open('tweet.txt', 'r')
print("the file contains:") 
print(a.read())

"""c.	For the User table file add a column that specifies how many tweets by that user are currently in the database. That is, your output file should contain all of the columns from the User table, plus the new column with tweet count. You do not need to modify the User table, just create the output text file. What is the name of the user with most tweets?"""

start= time.time()
f=open('user.txt', 'w')
for row in cfile.execute('''select user_id.*, count(tweet.user_id) 
                            from user_id,tweet 
                            where tweet.user_id =user_id.id 
                            Group by tweet.user_id
                            having count(tweet.user_id) ''').fetchall():
    
    f.write(str(row)[1:-1].replace(', ', '|')  + '\n')
f.close()
stop = time.time()
print("diff "+str(stop-start))
a = open('user.txt', 'r')
print("the file contains:") 
print(a.read())





