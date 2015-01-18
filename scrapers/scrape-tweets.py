# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 15:05:35 2015

@author: Talha Oz @tozCSS
"""

import pandas as pd
from bs4 import BeautifulSoup
import os

def nediyor_news():
    df = pd.DataFrame(columns=('twhandle', 'twtext', 'title',  'dt'))
    errors = []
    
    for html in (os.listdir('news/nediyor_news/')):
        print html,
        try:
            f = open('news/nediyor_news/'+html)
            soup = BeautifulSoup(f, "lxml")
            title  = soup.head.title.text.split('|')[0].strip()
            dt     = pd.to_datetime(soup.head.find("meta",{'property':'og:url'})['content'][19:29])
            twfeed = soup.findAll('div',attrs = {'class':'twitter-text'})
            for tw in twfeed:       
                links = tw.findAll('a')
                twhandle = links[1].text
                twtext = ''
                for i in range(3,6):
                    if links[i].text == '':
                        break
                    twtext += ' '+links[i].text
                df.loc[len(df)+1]=[twhandle,twtext,title,dt]
                # print twhandle,twtext,title,dt
            f.close()
            print dt,title
        except:
            errors.append(html)
    
    df.to_csv("TR-tweeps.csv",encoding='utf-8',index=False)
    print errors
    

def theplazz_news():
    df = pd.DataFrame(columns=('twhandle', 'twtext', 'title',  'dt'))
    errors = []
    
    for html in (os.listdir('news/theplazz_news/')):
        print html,
        try:
            f = open('news/theplazz_news/'+html)
            soup = BeautifulSoup(f, "lxml")
            title  = soup.head.title.text.split('|')[0].strip()
            dt     = pd.to_datetime(soup.body.find('div',{'class':'metaLinks'}).text.split('|')[0].split(':')[1])
            twfeed = soup.findAll('div',attrs = {'class':'tweet-body-text-single'})
            for tw in twfeed:       
                links    = tw.findAll('a')
                twhandle = links[1].text
                twtext   = links[2].text
                df.loc[len(df)+1]=[twhandle,twtext,title,dt]
                # print twhandle,twtext,title,dt
            f.close()
            print dt,title
        except:
            errors.append(html)
    
    df.to_csv("US-tweeps.csv",encoding='utf-8',index=False)
    print errors


def theplazz_get_dates():
    df = pd.DataFrame(columns=('newsdate','twcount', 'title',  'href'))
    errors = []
    
    for html in (os.listdir('news/theplazz_news/')):
        print html,
        try:
            f = open('news/theplazz_news/'+html)
            soup = BeautifulSoup(f, "lxml")
            title  = soup.head.title.text.split('|')[0].strip()
            meta = soup.body.find('div',{'class':'metaLinks'}).text
            dt     = pd.to_datetime(meta.split('|')[0].split(':')[1])
            twcount = int(meta.split('|')[1])
            href = soup.head.find("meta",{'property':'og:url'})['content']
            
            df.loc[len(df)+1]=[dt,twcount,title,href]
            f.close()
            print dt,href,title
        except:
            errors.append(html)
    
    df.to_csv("US-headlines.csv",encoding='utf-8',index=False)
    print errors

