#!/usr/bin/env python
# coding: utf-8

# # HW01

# In[1]:


import random
import math
import numpy as np
import pandas as pd


# a.	Write a function to generate a list of x random numbers in the range between 21 and 100 (similar to the genRandomMatrix code from the lecture, but only single-dimension).

# In[2]:


def genRandomlist(x):
    Randomlst=[random.randrange(21,101) for i in range(x)]
    return Randomlst


# In[3]:


random.seed(0)
genRandomlist(12)


# In[4]:


def genRandomlist(x):
    Randomlist=[]
    lst=[random.randrange(21,101) for i in range(x)]
    for num in lst:
        Randomlist.append(num)
    return lst


# In[5]:


random.seed(0)
genRandomlist(12)


# b.	Create a list of 50 random numbers with your code and use pandas.Series to determine how many of the numbers are below 33

# In[6]:


def numlow33():
    num=genRandomlist(50)
    seriesnum = pd.Series(num) 
    filter = seriesnum <33
    print(seriesnum[filter])
    print(len(seriesnum[filter]))


# In[7]:


random.seed(0)
numlow33()


# c.	Using the same list of 50 random numbers, 1) create a numpy array, modify it to 5x10 (you can do this by calling numpy.reshape(yourArray, (5,10)) and then replace all numbers that are greater than or equal to 33 by a string (‘33+’)

# In[8]:


random.seed(0)
fivetenmatrix = np.reshape(genRandomlist(50), (5,10)) 
print (np.where(fivetenmatrix >= 33, '33+', fivetenmatrix))


# d.	Use numpy to save the array into a CSV file (numpy.savetxt function)

# In[11]:


random.seed(0)
fivetenmatrix = np.reshape(genRandomlist(50), (5,10))
c = np.savetxt('npfile.cvs', fivetenmatrix, delimiter =', ')    
a = open("npfile.cvs", 'r')# open file in read mode 

print("the file contains:") 
print(a.read()) 


# 
# e.	Use pandas to read that txt file into a data frame (pandas.read_csv function). Note that you have to make sure the first line of data does not get misinterpreted as the header.

# In[12]:


import sys
frame  = pd.read_csv("npfile.cvs",header=None)
frame


# # HW02
# 

# In[13]:


import numpy as np
import pandas as pd
import sys


# In[14]:


myFD = open('Assignment4.txt', 'r')
Line = myFD.readline()
Line


# In[15]:


len(Line)


# In[16]:


tweet = Line.split('EndOfTweet')
tweet


# In[6]:


len(tweet)


# In[57]:


import json
for i in range(len(tweet)):
    tweets=json.loads(tweet[i])
tweets


# a.	Create a SQL table to contain the following attributes of a tweet:
# "created_at", "id_str", "text", "source", "in_reply_to_user_id", “in_reply_to_screen_name”, “in_reply_to_status_id”, "retweet_count", “contributors”. Please assign reasonable data types to each attribute and use SQLite for this assignment.
# 

# b.	Write python code to read through the Assignment4.txt file and populate your table from part a.  Make sure your python code reads through the file and loads the data properly (including NULLs).

# In[3]:


import sys

myFD = open('Assignment4.txt', 'r')
Line = myFD.readline()
tweet = Line.split('EndOfTweet')

import json
import sqlite3

conn = sqlite3.connect('dsc450_HW4.db')
c = conn.cursor()

tweettable = '''CREATE TABLE tweet(

    created_at Varchar2(100),
    id_str  Number(18),
    text Varchar2(100),
    source Varchar2(100), 
    in_reply_to_user_id Number(18),
    in_reply_to_screen_name Varchar2(100),
    in_reply_to_status_id Number(18),
    retweet_count Number(18),
    contributors Varchar2(100),
    
    
    CONSTRAINT C_PK
        PRIMARY KEY(id_str)
);'''

c.execute(tweettable)

for i in range(len(tweet)):
    tweets=json.loads(tweet[i])
    c.execute('INSERT INTO tweet VALUES(?,?,?,?,?,?,?,?,?)', [tweets['created_at'],tweets['id_str'],tweets['text'],tweets['source'],tweets['in_reply_to_user_id'],tweets['in_reply_to_screen_name'],tweets['in_reply_to_status_id'],tweets['retweet_count'],tweets['contributors']])
    
    


# In[4]:


print(c.execute('select * from tweet where id_str= 397513609728651265').fetchall())


# In[5]:


print(c.execute('select * from tweet where id_str= 397513609732816896').fetchall())


# a.	Count the number of iPhone users (based on “source” attribute)

# In[6]:


print(c.execute("select count(source) from tweet where source like'%iphone%'").fetchall())


# In[7]:


print(c.execute('select * from tweet where in_reply_to_user_id is NULL').fetchall())


# b.	Create a view that contains only tweets from users who are not replying ("in_reply_to_user_id" is NULL)

# In[45]:


print(c.execute('''Create view noreplytweet as select * from tweet where in_reply_to_user_id is NULL''').fetchall())


# In[9]:


print(c.execute(''' select * from noreplytweet ''').fetchall())


# c.	Select tweets that have a "retweet_count" higher than the average "retweet_count" from the tweets in the view in part b

# In[10]:


c.execute(''' select * from noreplytweet where retweet_count > avg(retweet_count)''').fetchall()


# In[11]:


c.execute(''' select * 
                from noreplytweet 
                where retweet_count > (select avg(retweet_count) from noreplytweet)''').fetchall()


# In[12]:


c.execute(''' Create view retweet_c5 as select id_str, text, source from tweet where retweet_count >= 5''').fetchall()


# e.	Use the view from part-d to find how many tweets have a “retweet_count” of at least 5

# In[14]:


c.execute(''' select count(*) from retweet_c5''').fetchall()


# f.	Write python code to compute the answer from 3-e without using SQL, i.e., write code that is going to read data from the input file and answer the same question (find how many tweets have a “retweet_count” of at least 5).

# In[16]:


def tweetleastfive():
    import sys
    import json

    myFD = open('Assignment4.txt', 'r')
    Line = myFD.readline()
    tweet = Line.split('EndOfTweet')
    leastfive=0
    
    for i in range(len(tweet)):
        tweets=json.loads(tweet[i])
        if tweets['retweet_count']>=5:
            leastfive+=1
    return leastfive

tweetleastfive()


# # 4.	Write a python function that takes the name of a SQL table as parameter and then does the following:

# In[47]:


def generateInsertStatements(table):
    data= c.execute('select * from '+ table).fetchall()
    d = open('inserts.txt','w')  
    for value in data:
        InsertStatements='INSERT INTO '+ table+' VALUES'+ str(value)+'\n'
        d.write(InsertStatements)
generateInsertStatements('tweet')
a = open("inserts.txt", 'r')# open file in read mode 
print("the file contains:") 
print(a.read()) 


# 5. Write a PL/SQL trigger that will cap the course number column in the university.sql database at 599. That is, any time an update or an insert would provide course number 600 or higher, automatically reset the value back to 599. Be sure to verify that your trigger is working with some sample data.. Write a PL/SQL trigger that will cap the course number column in the university.sql database at 599. That is, any time an update or an insert would provide course number 600 or higher, automatically reset the value back to 599. Be sure to verify that your trigger is working with some sample data.

# In[48]:


create or replace trigger course_number599 before insert or update on course for each row begin
if :new.CourseNr >599 then :new.CourseNr :=599;
 
end if; end;
()
insert into course
values ( 2983, 'in Digital Cinema', 'DC', 600);
insert into course
values ( 2943, 'ML', 'DC', 700);
select * from course





