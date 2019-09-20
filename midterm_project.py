
# coding: utf-8

# Hypothesis: The top 3 factories(various) that affect the house sale prices are
# total Rooms above ground(TotalRAG), 
# Ground living area(GrLivArea) and 
# Overall quality(OverallQual)
# Source: https://www.kaggle.com/c/house-prices-advanced-regression-techniques

# In[1]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


# In[2]:


#Getting Data
df=pd.read_csv('house price.csv')


# In[3]:


#Basic Info
df.info()


# Data cleaning
# First, take a look at the missing rate of each feature. As we can be seen from the table below, the missing rate of PoolQC, MiscFeature, Alley and Fence is particularly high, and fireplacenta has reached about half. It can be consider removing these features when preprocessing.

# In[4]:


#View missing value of columns
df.isnull().any().sum()


# In[5]:


#Checking for NaN
N=pd.concat([df.dtypes,df.isnull().sum(),df.isnull().sum()/df.shape[0]], 
                 axis=1,keys=['dtype','total','percentage'])
N_sort=N.sort_values(['percentage'],axis=0,ascending=False)
#Print the NaN count greater than zero
N_sort.head(20)


# In[6]:


#Remove top 5 high fault rate data
df.drop(columns=['PoolQC','MiscFeature','Alley','Fence','FireplaceQu'],axis=1)


# Analyze target variables
# The target variable is continuous and has no special outlier (0 or negative). 
# There is no invalid or other non-numeric data.

# In[7]:


#Summary of descriptive statistics of sale price
df['SalePrice'].describe()


# In[8]:


#Target visualization
_=sns.distplot(df['SalePrice'],color='purple')


# Selecting the 3 features from hypothesis related to the target variable SalePrice.
# For continuous variables, the Pearson correlation coefficient can be used to find the features relevant to the target variables.Pearson correlation coefficient is a statistic describing the degree of linear correlation between two continuous variables. Its value range is [-1,+1].
# 
# For numerical type, we are more concerned with the relationship and distribution between each feature and the target variable. The scatter diagram can be adopted to visually check outliers.

# In[9]:


#TotRmsAbvGrd
df2=df
j=sns.jointplot("TotRmsAbvGrd","SalePrice",data=df2,kind="reg")


# In[10]:


#GrLivArea
df3=df
j=sns.jointplot(x="GrLivArea",y="SalePrice",data=df3,kind="reg")


# In[11]:


#OverallQual
df4=df
j=sns.jointplot(x="OverallQual",y="SalePrice",data=df4,kind="reg")

It can be seen from the above figure that the housing price is a linear relationship with the those three features.
# Using a method for systematic analysis of the correlation between each features and the target variables. 
# Analyzing the overall features (numerical data) of the data set to find the best result.
# Calculating the correlation coefficient by using .corr(), and then show the heatmap with correlation.

# In[12]:


#Get numeric columns for visualization
numeric_columns=df.dtypes[df.dtypes!='object'].index


# Correlation matrix visualization use color and value to represent the correlation between any two elements. 
# The lighter the color, the stronger the correlation, vice versa.

# In[13]:


#Correlation matrix
df1=df
corrmat=df1[numeric_columns].corr()
hm=sns.heatmap(corrmat,vmax=1,linewidths=0.01,square=True,annot=True,linecolor='white',cmap='pink')
hm.figure.set_size_inches(25,25)


# Select the pearson correlation coefficients features of the top 10 features

# In[14]:


#Saleprice correlation matrix 
k=10
cl=corrmat.nlargest(k,'SalePrice')['SalePrice'].index
cm=np.corrcoef(df[cl].values.T)
hm=sns.heatmap(cm,cbar=True,annot=True,cmap='pink',annot_kws={'size': 10},yticklabels=cl.values,xticklabels=cl.values)
hm.figure.set_size_inches(10,10)


# The correlation between two identical elements is 1, such as saleprice and saleprice. We can see from the figure that the correlation between garagecars and garagearea is 0.88, indicating the two elements are highly correlated. We can take one element characteristic, similar to totalbsmtSF and 1stFlrSF(0.82).
# Just keep 'GarageCars' and 'TotalBsmtSF'.

# 'OverallQual'(0.79) and 'GrLivArea'(0.71) are strongly correlated with 'SalePrice'.
# 'GarageCars'(0.64) and 'TotalBsmtSF'(0.61) are moderate positive correlation.

# Conclusion:
# The result of hypothesis of pearson correlation coefficient:
# 'TotRmsAbvGrd'(0.53), 
# 'GrLivArea'(0.71),
# 'OverallQual'(0.79).
# The result of top 3 of pearson correlation coefficient:
# 'OverallQual'(0.79), 
# 'GrLivArea'(0.71) ,
# 'GarageCars'(0.64).
# The hypothesis are too close with the result of actual data analysis, due to the continuous variable has positive correlations with sale price.
# Lesson Learned:
# It is time-consuming and tedious to analyze individual features with target variables one by one. Using heatmap to analyze the correlation between the characteristics and the target variables is claer and easier.
# Need to improve:
# Considering the model is overfitting ot not and dealt with data outliers.
