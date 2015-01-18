# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 15:41:01 2015

@author: Talha
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

#initialize variables
df = pd.DataFrame(columns=('title', 'twcount', 'href'))
driver = webdriver.Chrome()

# thePlazz.com Headlines 'http://theplazz.com/category/headlines/'
driver.get('file:///Users/toz/Documents/workspace/TR-2014/data/thePlazz.html')
time.sleep(60) #have to wait till the page is loaded completely

# This is how I retrieved thePlazz.html file, i.e.
# I added the two lines above for your convenience, myself never used
#driver.get('http://theplazz.com/category/headlines/')
#for i in range(600):
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    time.sleep(3)


news = driver.find_elements_by_xpath("//div[@class='post-top']")
for i,haber in enumerate(news):
    title = haber.find_element_by_tag_name("h3").find_element_by_tag_name("a")
    twcount = int(haber.find_element_by_xpath("div[@class='post-meta']").find_element_by_tag_name("a").text)
    print i, title.text , twcount, title.get_attribute("href")
    df.loc[len(df)+1]=[title.text , twcount, title.get_attribute("href")]

df['twcount']=df['twcount'].astype(int)
df.to_csv("US-news-org.csv",encoding='utf-8',index=False)