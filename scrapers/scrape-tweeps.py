# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 09:08:17 2015

@author: Talha
"""

import pandas as pd
#import wget

df = pd.read_csv('data/TR-tweeps.csv',usecols=['twhandle','twtext'],encoding='utf-8')
tweeps = df.groupby('twhandle').count().sort('twtext').index.tolist()
del tweeps[0]
urls = ['http://nediyor.com/'+tw[1:] for tw in tweeps]
f=open('urls.txt', 'w+')
for url in urls:
    print >>f,url
    #wget.download(url,out='tweeps')
f.close()
#nohup sh -c "cat urls.txt | xargs -n 1 -P 10 wget " &
#zip nediyor_tweeps.zip *

from bs4 import BeautifulSoup
import os

df = pd.DataFrame(columns=('twhandle', 'name', 'fcnt', 'profs'))
errors = []
    
for html in (os.listdir('nediyor_tweeps/')):
    print html,
    try:
        f = open('nediyor_tweeps/'+html)
        soup = BeautifulSoup(f, "lxml")
        info = soup.find('div',attrs = {'class':'col-sm-8'})
        name = info.h2.text.strip()
        twhandle = info.span.text.strip()
        profs = info.findAll('span','label label-default')
        profs = ', '.join([prof.text for prof in profs])
        fcnt= soup.find('a',{'id':'user-members-followers'}).span.text
        print twhandle, name, fcnt, profs
        df.loc[len(df)+1]=[twhandle, name, fcnt, profs]
        f.close()
    except:
        errors.append(html)

df.to_csv("data/TR-tweeps.csv",encoding='utf-8',index=False)
print errors