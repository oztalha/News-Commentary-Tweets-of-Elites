
# coding: utf-8

# # 113th Congress as News Commentators on Twitter
# 
# In this project I am answering the following questions:
# 
# * Who are the most active news commentators among senators and congressmen ?
# * Which news got the most attention by the politicians ?
# * How many news (of 7376) are commentated by democrats and/or republicans...
# * How many comments made on these news by each group ?
# * What are the news with the highest difference of comment counts (of groups)?
# 
# The news and the curated tweets used in this study are scraped from theplazz.com approximately matching the duration of [113th US Congress](https://en.wikipedia.org/wiki/113th_United_States_Congress), i.e. between Jan 2013 - Jan 2015.
# 
# See [here](http://talhaoz.com/news/) for other iPython notebooks on this project.
# 
# Project (datasets and the source code) is available on [GitHub](https://github.com/oztalha/News-Commentary-Tweets-of-Elites)
# 

# In[2]:

import twitter
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from mykeys import tw


# In[3]:

def oauth_login():
    """Twitter authorization """
    #tw is a dictionary, the only variable in mykeys.py
    auth = twitter.oauth.OAuth(tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'],
             tw['CONSUMER_KEY'], tw['CONSUMER_SECRET'])
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def get_members(members):
    """Scrape only the interesting info from twitter json response """
    return [(m['id'],m['screen_name'],m['name'],m['location'],m['description'],
            m['created_at'], m['friends_count'],m['followers_count'],
            m['statuses_count'],m['favourites_count']) for m in members['users']]


def tw_to_pol(twitter_api,slug,owner_screen_name,group):
    """Get members of a twitter list with known political group into a dataframe """
    resp = twitter_api.lists.members(slug=slug,owner_screen_name=owner_screen_name,cursor=-1,count=5000)
    members = get_members(resp)
    df = pd.DataFrame(members,columns=header)
    df['party'] = group
    return df


def get_politicians():
    """Download 113th congress tweeps using public Twitter lists"""

    header = ['id','screen_name','name','location','description','created_at',
           'friends','followers','statuses','favorites']

    polists = [{'slug':'senaterepublicans', 'owner_screen_name':'Senate_GOPs', 'group':'gop'}, #62
               {'slug':'house-republicans', 'owner_screen_name':'HouseGOP', 'group':'gop'}, #260
               {'slug':'housegop', 'owner_screen_name':'GOPLeader', 'group':'gop'}, #237
               {'slug':'elected-democrats', 'owner_screen_name':'TheDemocrats', 'group':'dem'}, #259
               {'slug':'house-democrats', 'owner_screen_name':'DannyMariachi', 'group':'dem'}, #188
               {'slug':'senatedemocrats', 'owner_screen_name':'SenateDems', 'group':'dem'} #52
              ]
    
    twitter_api = oauth_login()

    df = pd.DataFrame(columns=header)
    for polist in polists:
        df = df.append(tw_to_pol(twitter_api,polist['slug'],polist['owner_screen_name'],polist['group']))
    df = df.drop_duplicates()
    df.to_csv('data/US-politicians.csv',encoding='utf-8',index=False)
    return df


# In[4]:

# get twitter IDs of congressmen and senators
df = pd.read_csv('data/US-politicians.csv',encoding='utf-8')
gop = df[df['party']=='gop']
dem = df[df['party']=='dem']
dem_tweeps = set(dem.screen_name.values)
gop_tweeps = set(gop.screen_name.values)
# Principal Accounts of Members of the U.S. Senate (a mix of campaign and government accounts)
senate = pd.read_csv('data/US-senate.csv',encoding='utf-8')


# In[5]:

# get commentary tweets of US newsmakers and opinion-shapers
tweets = pd.read_csv('data/US-tweets.csv',encoding='utf-8')
tweets.twhandle = tweets.twhandle.str[1:]


# In[6]:

# print politician counts curated at least once by theplazz.com
tweepset = set(tweets.twhandle.unique())
senateset = set(senate.screen_name.values)
print('curated senator count:',len(senateset & tweepset))
print('curated democrat count:',len(dem_tweeps & tweepset))
print('curated republican count:',len(gop_tweeps & tweepset))


# In[7]:

# plot commentating activity of these politicians
tweeps = tweets.groupby(by='twhandle')['twtext'].count().order(ascending=False)
poltweeps = tweeps[tweeps.index.isin(df.screen_name)]
colors = ['blue' if x in dem_tweeps else 'red' for x in poltweeps.index]
data = Data([Bar(
        x=poltweeps.index,
        y=poltweeps.values,
        marker=Marker(color=colors)
        )])
layout = Layout(yaxis=YAxis(title='# of news commentated (Jan 2013 - Jan 2015)'),
                title="News counts commentated by 113th US Congress (curated by theplazz.com)")
fig = Figure(data=data, layout=layout)
py.iplot(fig,filename="113th US Congress as News Commentators")


# In[8]:

# how many news are commentated by how many democrats and/or republicans...
title = tweets.groupby(by=['title','dt'])['twhandle']
demnews = title.apply(lambda g: len(dem_tweeps & set(g.values)))
gopnews = title.apply(lambda g: len(gop_tweeps & set(g.values)))
print (demnews.sum(),'comments made on',demnews[demnews>0].size,'news by democrats.')
print (gopnews.sum(),'comments made on',gopnews[gopnews>0].size,'news by republicans.')
dgtotl = (demnews + gopnews)
print ('News commentated by either group:',(dgtotl[dgtotl>0].size))
both = demnews & gopnews
print ('News commentated by both parties:',(both[both==True].size))


# In[9]:

# Which news got the most attention by the politicians ?
dgtotl.order(ascending=False).head(60)


# In[10]:

# On which news the comment-count differences maximized?
# Number of comments by gop - number of comments by dems
dgdiff = (demnews - gopnews)
dgdiff.order()
