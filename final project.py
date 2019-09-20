
# coding: utf-8

# In[1]:


Theme: 
TMDB 5000 Movie Dataset
data source location: 
https://www.kaggle.com/tmdb/tmdb-movie-metadata
size of data: 
4803 rows x  24 columns, 9 MB
Hypothesis: 
The relase date of movie make higher profit is August.
The movie genres of comedies make higher profit.
Explain:
The datasets contains basic information of movie and average vote score in between 1920 to 2017 of many countries. Among them, I will do data pre-processing and cleaning, feature analysis and visualization. 


# In[ ]:


import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import requests
plt.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df1 = pd.read_csv('tmdb_5000_movies.csv')
df2 = pd.read_csv('tmdb_5000_credits.csv')
df1.head(2)


# In[ ]:


df2.head(2)


# In[ ]:


#merge 2 CSV
df = df2.merge(right=df1,how='inner',left_on='movie_id',right_on='id')
df.head()


# In[ ]:


#check basic info
df.info()


# In[ ]:


#Checking for NaN
N=pd.concat([df.dtypes,df.isnull().sum(),df.isnull().sum()/df.shape[0]], 
                 axis=1,keys=['dtype','total','percentage'])
N_sort=N.sort_values(['percentage'],axis=0,ascending=False)
#Print the NaN count greater than zero
N_sort.head(20)


# In[ ]:


#Remove top 2 high fault rate data and inconsiderable data 
del df['homepage']
del df['tagline']
del df['id']
del df['original_title']
df.head()


# In[ ]:


#check missing data of runtime
N=df['runtime'].isnull()
df.loc[N,:]


# In[ ]:


#check missing data of release date
N=df['release_date'].isnull()
df.loc[N,:]


# In[ ]:


df.loc[df['release_date'].isnull()==True]
#fill in missing date by online searching, March 1st,2015
df['release_date'] = df['release_date'].fillna('2015-03-01')

df.loc[df['runtime'].isnull()==True]
#fill in missing runtime by online searching, 113mins and 81 mins respectively
df['runtime'] = df['runtime'].fillna(113, limit=1)
df['runtime'] = df['runtime'].fillna(81, limit=1)
#limit to fill in one value once


# In[ ]:


#View processing results
df.info()


# In[ ]:


df[['runtime','popularity','vote_average','vote_count','budget','revenue']].corr()


# In[ ]:


revenue = df[['popularity','vote_count','budget','revenue']]


# In[ ]:


df.revenue.describe()


# In[ ]:


df.budget.describe()


# In[ ]:


df['profit']=df['revenue']-df['budget']


# In[ ]:


import seaborn as sns
sns.heatmap(df.corr(), annot=True, vmax=1, square=True, cmap='Purples')


# In[ ]:


# changing the genres column from json to string
df['genres']=df['genres'].apply(json.loads)
for index,i in zip(df.index,df['genres']):
    list1=[]
    for j in range(len(i)):
        list1.append((i[j]['name']))# the key 'name' contains the name of the genre
    df.loc[index,'genres']=str(list1)


# In[ ]:


df.head(2)


# In[ ]:


df['genres'][1].split(',')#split分隔字符串


# In[ ]:


genre = set()
for i in df['genres'].str.split(','):
    genre=set().union(i,genre)


# In[ ]:


#转化为列表
genre=list(genre)
genre


# In[ ]:


#for循环   genre是一个list   genr是一个str
for genr in genre:
    df[genr] = df['genres'].str.contains(genr).apply(lambda x:1 if x else 0)
#str.contains(genr）字符串包含，然后用一个密函数判断


# In[ ]:


df_gen_pro=pd.DataFrame(index=genre)


# In[ ]:


profit_df = pd.DataFrame()#创建空的数据框
profit_df = pd.concat([genre_df.iloc[:,:-1],full['profit']],axis=1)  #合并
profit_df.head()#查看新数据框信息


# In[ ]:


#求出每种类型的平均利润
list=[]#建立一个列表
#创建一个循环  list.append（）方法用于在列表末尾添加新的对象
for genr in genre:
    list.append(df.groupby(genr)['profit'].mean())
list2=[]
#range(len(list_1))遍历一个list
for i in range(len(genre)):
    list2.append(list[i][1])
df_gen_pro['mean_profit']=list2


# In[ ]:


df_gen_pro.sort_values(by='mean_profit',ascending=True).plot.barh(label='genre',figsize=(15,7))
plt.title('电影类型的利润条形图',fontsize=20)
plt.xlabel('profit',fontsize=20)
plt.ylabel('genres',fontsize=20)
plt.grid(True)
plt.show()


# In[ ]:


plt.figure(figsize=(6,4))
plt.plot(kind='barh')
plt.title('genres profit')
plt.xlable('amount')
plt.show()


# In[ ]:


df.sort_values('revenue', ascending=False)[['title', 'revenue', 'budget', 'genres']][0:10]


# ### 
