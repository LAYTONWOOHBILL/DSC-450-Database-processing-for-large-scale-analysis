#!/usr/bin/env python
# coding: utf-8

# b.	Write python code that is going to read and load the Assignment5.txt file from the web and populate both of your tables (Tweet table from Assignment4 and User table from this assignment). You can use the same code from the previous assignment with an additional step of inserting into the new table.

# In[2]:


import sys
import json
import urllib
import sqlite3
webFD=urllib.request.urlopen ("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/Assignment5.txt")
alltweet=webFD.readlines()
conn = sqlite3.connect('dsc450_HW5.db')
c = conn.cursor()

usertable = '''CREATE TABLE user_id(

    id         Number(18),
    name       Varchar2(100),
    screen_name  Varchar2(100),
    description  Varchar2(100),
    friends_count  Number(18)

);'''

tweettable = '''CREATE TABLE tweet(
    created_at text,
    id_str  int,
    text  text,
    source  text, 
    in_reply_to_user_id int,
    in_reply_to_screen_name  text,
    in_reply_to_status_id int,
    retweet_count int,
    contributors  text,
    geo text,
    user_id  int
    
);'''

try:
    c.execute('drop table tweet')
    c.execute('drop table user_id')
except:
    pass


c.execute(usertable)
c.execute(tweettable)
d = open('Assignment5_errors.txt','w')

user_list, tweet_list = [], []

for tweet in alltweet:
    try:
        tdict = json.loads(tweet.decode('utf8'))
    except:
        d.write(tweet.decode('utf8'))
    else:
        user_list.append((tdict['user']['id'],tdict['user']['name'],tdict['user']['screen_name'],tdict['user']['description'],tdict['user']['friends_count']))
        
        if tdict['geo'] != None:
            tweet_list.append((tdict['created_at'],tdict['id_str'],
                           tdict['text'],tdict['source'],tdict['in_reply_to_user_id'],
                           tdict['in_reply_to_screen_name'],tdict['in_reply_to_status_id'],
                           tdict['retweet_count'],tdict['contributors'],tdict['geo']['type'],tdict['user']['id_str']))
        else:
            tweet_list.append((tdict['created_at'],tdict['id_str'],
                           tdict['text'],tdict['source'],tdict['in_reply_to_user_id'],
                           tdict['in_reply_to_screen_name'],tdict['in_reply_to_status_id'],
                           tdict['retweet_count'],tdict['contributors'],tdict['geo'],tdict['user']['id_str']))
            

c.executemany('INSERT INTO user_id VALUES(?,?,?,?,?)',user_list)
c.executemany('INSERT INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)',tweet_list) 
d.close()


# In[3]:


for geopoint in c.execute('select * from tweet where geo != "None"').fetchall():
    print(geopoint)


# In[4]:


print(c.execute('select count(*) from tweet where geo is NULL').fetchall())
for geonone in c.execute('select * from tweet where geo is NULL').fetchall():
    print(geonone)


# In[5]:


tweet_nogeo=[]
for tweet in alltweet:
    try:
        tdict = json.loads(tweet.decode('utf8'))
    except:
        pass
    else:
        if tdict['geo'] == None:
            tweet_nogeo.append((tdict['created_at'],tdict['id_str'],
                           tdict['text'],tdict['source'],tdict['in_reply_to_user_id'],
                           tdict['in_reply_to_screen_name'],tdict['in_reply_to_status_id'],
                           tdict['retweet_count'],tdict['contributors'],tdict['geo'],tdict['user']['id_str']))
            
print(len(tweet_nogeo))           
for t in tweet_nogeo:
    print(t)


# a.	Write and execute SQL query that finds the longest and the shortest tweet text message (if there is a tie, you must return all shortest and longest tweet messages, not just one). This is SQL-only, using your SQLite database.!

# In[411]:


for ltwe in c.execute('''select text from tweet 
                      where length(text) = (select min(length(text))from tweet)''').fetchall():
    print(ltwe)
    
for stwe in c.execute('''select text from tweet 
                      where length(text) = (select max(length(text))from tweet)''').fetchall():
    print(stwe)

print(c.execute('''select max(length(text))from tweet''').fetchall())


# In[10]:


tweet_len=[]
for tweet in alltweet:
    try:
        tdict = json.loads(tweet.decode('utf8'))
    except:
        pass
    else:
        if len(tdict['text']) == 1:
            tweet_len.append((len(tdict['text']),tdict['text']))
        elif len(tdict['text']) == 164:
            tweet_len.append((len(tdict['text']),tdict['text']))    
print(sorted(tweet_len, key=lambda tup:(tup[0])))


# b.	Use python to plot the lengths of first 100 tweets (only 100, not all of the tweets) versus the length of the username for the user on a graph. Use a scatterplot.!

# In[334]:


import matplotlib.pyplot as plt
fig=plt.figure()
tweetplot = fig.add_subplot(2,2,1)
fig.set_size_inches(30,18)

for i in range(100):
    try:
        tweet = alltweet[i]
        tdict = json.loads(tweet.decode('utf8'))
    except:
        pass
    else:
        tweetplot.scatter(len(tdict['text']),len(tdict['user']['name']))


# In[335]:


word=[]
for tweet in alltweet:
    try:
        tdict = json.loads(tweet.decode('utf8'))
    except:
        pass
    else:
        word.append(tdict['text'])
counts = dict()
for sting in word:
    a = sting.split(' ')
    for i in a:
        if len(i)>=6:
            counts[i] = counts.get(i, 0) + 1
            
counts
orderdata = sorted(counts.items(), key=lambda item: -item[1])
print('This is top-5 most frequent terms:  ')
for num in range(5):
    print(orderdata[num])
    
#for key, value in sorted(counts.items(), key=lambda item: -item[1]):
#    print("%s: %s" % (key, value))
#sorted(counts, key=lambda tup:(tup[0]))


# In[15]:


tdict


# In[ ]:




