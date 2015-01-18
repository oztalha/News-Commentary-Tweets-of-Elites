# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 16:42:40 2015

@author: Talha
"""
import pandas as pd

df = pd.read_csv('data/TR-tweeps.csv',encoding='utf-8')
# df = pd.read_csv('TR-commentators.csv',encoding='utf-8',skiprows=[143914])
# order commentators by total number of comments in two years
df.groupby(by='twhandle')['twtext'].count().order(ascending=False).to_csv('US-tweep-comment-counts.csv',header=True)