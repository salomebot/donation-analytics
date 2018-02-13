
# Import Dependencies
import math
from collections import Counter
import csv
import pandas as pd
import numpy as np
import os
import time
from scipy import stats
from datetime import datetime
import datetime as dt

# Set Start date and Current date of this Analysis
start_date= pd.to_datetime('01012015', format="%m%d%Y")
type(start_date)

current_date=pd.to_datetime('now')
x=current_date.year-start_date.year
# print(range(x+1))

#Download Input Files, Percentile and Input

percentile = pd.read_csv('./input/percentile.txt', sep="|",error_bad_lines=False, 
                   index_col=False, dtype='unicode', header=None, encoding="utf-8") 
percentile[0]

data = pd.read_csv('./input/itcont.txt', sep="|",error_bad_lines=False, 
                   index_col=False, dtype='unicode', header=None) 
data.head()

#Create a Dataframe and Select Columns to be analysed. For convinience, renamed with specific title

data_df=data[[0,7,10,13,14,15]]
data_df=data_df.rename(index=str, columns={0: "CMTE_ID", 7: "NAME", 10:"ZIP_CODE",13:"TRANSACTION_DT",14:"TRANSACTION_AMT",15:"OTHER_ID"})
data_df.head()
data_df

#Clean the Dataframe
#Remove empty fields and NAN (except in "OTHER_ID")
#Select only "CMTE_ID" With characters of length 9
#Select only 'TRANSACTION_DT' with characters of length 8


data_df[(data_df !="").any(axis=1)]


data_df = data_df[(data_df['CMTE_ID'].notnull())
                  &(data_df['NAME'].notnull())&(data_df['ZIP_CODE'].notnull())
                   &(data_df['TRANSACTION_DT'].notnull())&(data_df['TRANSACTION_AMT'].notnull())
                  &(data_df['OTHER_ID'].isnull())]
data_df=data_df[(data_df['CMTE_ID'].apply(lambda x: len(x)==9))]
data_df=data_df[(data_df['TRANSACTION_DT'].apply(lambda x: len(x)==8))]

#Select only 'ZIPCODE' with  characters with a length >=5 and show only the first 5 numbers
data_df=data_df[(data_df['ZIP_CODE'].apply(lambda x: len(x)>=5))]
data_df["ZIP_CODE"]=data_df["ZIP_CODE"].str[:5]
data_df

#Convert 'TRANSACTION_DT' to datetime

data_df['TRANSACTION_DT'] = pd.to_datetime(data_df['TRANSACTION_DT'], errors='coerce', format='%m%d%Y')


# Select the Data in the Dataframe only in between the Start_date and Current_date


data_df = data_df[(data_df["TRANSACTION_DT"] >= start_date ) & (data_df["TRANSACTION_DT"] <= current_date)]

#Create a new column with combine data from the "NAME" and "ZIP_CODE"
#Find duplicates on this new columns
data_df["NAME_ZIP_CODE"] = data_df[['NAME', 'ZIP_CODE']].apply(lambda x: ''.join(x), axis=1)
data_df

data_df = data_df[data_df.duplicated(['NAME_ZIP_CODE'], keep=False)]

data_df=data_df.reset_index(drop=True)
data_df
#Format the "TRANSACTION_DT" to show only the year

data_df["TRANSACTION_DT"]=data_df["TRANSACTION_DT"].dt.year

#Sort the values bY the "NAME_ZIP_CODE" column

data_df = data_df.sort_values(by=['NAME_ZIP_CODE']).reset_index(drop=True)
data_df

#Select only the data  where repeated donors donations are in correct chronological order and update the dataframe

x=[]
for j in range(len(data_df['NAME_ZIP_CODE'])-1):
    if (data_df.iloc[j]['NAME_ZIP_CODE'] == data_df.iloc[j+1]['NAME_ZIP_CODE'])and (data_df.iloc[j+1]['TRANSACTION_DT'] >= data_df.iloc[j]['TRANSACTION_DT']):
        x.append(j+1)
        # print(j+1)
        j += 1



data_df=data_df.iloc[x, :].reset_index(drop=True)

data_df


# In[618]:


y=[]
for i in range(len(data_df['NAME_ZIP_CODE'])-1):
    if (data_df.iloc[i]['NAME_ZIP_CODE'] == data_df.iloc[i+1]['NAME_ZIP_CODE'])and (data_df.iloc[i+1]['TRANSACTION_DT'] < data_df.iloc[i]['TRANSACTION_DT']):
        #frame_df["Y"] = frame_df["Y"].drop([i+1])
        y.append(i)
        y.append(i+1)
        #print(i+1)
        i += 1

#print(y)


data_df=data_df.drop(data_df.index[y])

#Remove the entrance in the Dataframe that happen in the year of the starting date
data_df=data_df[data_df.TRANSACTION_DT != start_date.year]

data_df


# Format the "TRANSACTION_AMT" data into floats and calculate the cumulative sum of the donations per donor per year


data_df['TRANSACTION_AMT']=data_df['TRANSACTION_AMT'].astype(float)

data_df = data_df.sort_values(by=['CMTE_ID','TRANSACTION_DT']).reset_index(drop=True)

data_df["CumSum"]= data_df["TRANSACTION_AMT"].cumsum().astype(int)

data_df

# Calculate the requested percentile on the input file of the donations per donor per year

percentile[0]=percentile[0].astype(int)

data_df["Percentile"]=data_df["TRANSACTION_AMT"].expanding().quantile((percentile[0]/100),interpolation='nearest').reset_index(level=0, drop=True).astype(int) 

# Calculate the total of donations the per for each candidate per donor per year

data_df["Total_donors"]=data_df['NAME_ZIP_CODE'].expanding().count().reset_index(level=0, drop=True).astype(int)

# Select only the Columns with the data corresponding to:"CMTE_ID','TRANSACTION_DT', "ZIP_CODE", "Percentile", "Cumsum", "Total Donors"

F=data_df.iloc[:, [0,2,3,8,7,9]]

data_df=F.reset_index(level=0, drop=True)
data_df

#Output the result as txt file in output folder

data_df.to_csv('./output/repeat_donors.txt', index=False, header=False,sep="|")

