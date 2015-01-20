import pandas as pd
from bs4 import BeautifulSoup
import os

def nediyor_news():
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []

    for i,html in enumerate(os.listdir('news/nediyor_news/')):
        try:
            f = open('news/nediyor_news/'+html)
            soup = BeautifulSoup(f, "lxml")
            title  = soup.head.title.text.split('|')[0].strip()
            href   = soup.head.find("meta",{'property':'og:url'})['content']
            dt     = pd.to_datetime(href[19:29],unit = 'D')
            newstxt = soup.find('div',attrs = {'class':'entry-content'}).text
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print len(errors),dt, title, href
            f.close()
        except:
            errors.append((i,html))
    
    df.to_csv("data/TR-news.csv",encoding='utf-8',index=False)
    print errors

def theplazz_news():
    df = pd.DataFrame(columns=('dt', 'title', 'href', 'newstxt'))
    errors = []
    
    for i,html in enumerate(os.listdir('news/theplazz_news/')):
        try:
            f = open('news/theplazz_news/'+html)
            soup = BeautifulSoup(f, "lxml")
            title  = soup.head.title.text.split('|')[0].strip()
            meta = soup.body.find('div',{'class':'metaLinks'}).text
            dt     = pd.to_datetime(meta.split('|')[0].split(':')[1])
            href = soup.head.find("meta",{'property':'og:url'})['content']
            newstxt = soup.find('div',attrs = {'class':'post-entry'}).text
            
            df.loc[len(df)+1]=[dt, title, href, newstxt]
            print len(errors),dt, title, href
            f.close()
        except:
            errors.append(i,html)
    
    df.to_csv("US-news.csv",encoding='utf-8',index=False)
    print errors