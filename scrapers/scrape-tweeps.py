# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 09:08:17 2015

@author: Talha
"""

def TR_tweep_URLs():
    """Create a URL list from twhandles"""
    import pandas as pd
    df = pd.read_csv('data/TR-tweeps.csv',usecols=['twhandle','twtext'],encoding='utf-8')
    tweeps = df.groupby('twhandle').count().sort('twtext').index.tolist()
    del tweeps[0]
    urls = ['http://nediyor.com/'+tw[1:] for tw in tweeps]
    f=open('urls.txt', 'w+')
    for url in urls:
        print >>f,url
    f.close()
    #nohup sh -c "cat urls.txt | xargs -n 1 -P 10 wget " &
    #zip nediyor_tweeps.zip *
    

def scrape_TR_tweeps_info():
    """Scrape tweeps info from nediyor_tweeps.zip
    
    I deceompressed the zip to a folder, and reading from it
    note: these files are indeed the outputs of TR_tweep_URLs()
    """
    from bs4 import BeautifulSoup
    import os
    import pandas as pd
    
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

def fix_tweep_profession():
    """There were some fixes needed on the raw data"""
    import pandas as pd
    df = pd.read_csv('data/TR-tweeps.csv',encoding='utf-8')
    gr = df.groupby('profs').count().sort('twhandle')
    pol = df.profs.str.contains(u'Politikacı').fillna(False)
    print df[pol].to_string()
    pr = set()
    for i in gr.index:
        a = i.split(',')
        pr.update([p.strip() for p in a])

    """
    print df[df.profs.isnull()].to_string()
    df.loc[149,'profs'] = u'İş kadını'
    df.loc[264,'profs'] = u'Müzisyen'
    df.loc[328,'profs'] = u'Sunucu'
    df.loc[459,'profs'] = u'AK Parti, Politikacı'
    df.loc[463,'profs'] = u'Taraftar lideri'
    df.loc[816,'profs'] = u'Yazar'
    df.loc[1031,'profs'] = u'İş adamı'
    df.loc[1197,'profs'] = u'Sunucu'
    """   
    df = df.replace(u'K\xf6\u015fe Yazar\u0131',u'K\xf6\u015fe yazar\u0131',regex=True)
    df.profs = df.profs.replace(u'BDP',u'HDP',regex=True)
    df.profs = df.profs.replace(u'Müzisyen',u'Şarkıcı',regex=True)

    df.to_csv("data/TR-tweeps.csv",encoding='utf-8',index=False)
    """
    TODO:
    parties = ['AK Parti','CHP','HDP','MHP',u'Bağımsız']
    mps = set()
    for p in parties:
        mps = mps | d[p]
    mps.difference(d['Milletvekili'])
    d['Milletvekili'].difference(mps)

    """

