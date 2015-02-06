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

def get_tweeps_by_profession():
    """Translates professions into English and groups them"""
    from collections import defaultdict
    import pandas as pd

    import plotly.plotly as py
    import plotly.tools as tls
    from plotly.graph_objs import *
    
    df = pd.read_csv('data/TR-tweeps.csv',encoding='utf-8')
    d = defaultdict(set)
    for i,r in df.iterrows():
        profs = r.profs.split(',')
        [d[prof.strip()].add(r.twhandle) for prof in profs]

    sorted_d = sorted(d.items(), key=lambda x: len(x[1]))
    profs, tweeps = zip(*sorted_d)
    """
    from unidecode import unidecode
    for p in profs:
        profs_en.append(json.load(urllib2.urlopen('http://cevir.ws/v1?q='+unidecode(p)+'&m=25&p=exact&l=tr')))
    profs_en[0] = 'Economist'
    profs_en[1] = 'Entrepreneur'
    profs_en[2] = 'Thinker'
    profs_en[3] = 'TV producer'
    profs_en[4] = 'Scientist'
    profs_en[5] = 'Poet'
    profs_en[6] = 'Cheerleader'
    profs_en[7] = 'PR specialist'
    profs_en[8] = 'Emeritus Officers'
    profs_en[9] = 'Religious Scholar'
    profs_en[10] = 'Coach'
    profs_en[11] = 'Others'
    profs_en[12] = 'Radio DJ'
    profs_en[13] = 'Sports club'
    profs_en[14] = 'Scientist'
    profs_en[15] = 'Adman'
    profs_en[16] = 'Independent MP'
    profs_en[17] = 'Emeritus bureaucrat'
    profs_en[18] = 'Lawyer'
    profs_en[19] = 'Legist'
    profs_en[20] = 'Movie Actor'
    profs_en[21] = 'MHP'
    profs_en[22] = 'HDP'
    profs_en[23] = 'Model'
    profs_en[24] = 'Stylist'
    profs_en[25] = 'Businesswoman'
    profs_en[26] = 'Consultant'
    profs_en[27] = 'Executive'
    profs_en[28] = 'Theater Actor'
    profs_en[29] = 'Director'
    profs_en[30] = 'Social entrepreneur'
    profs_en[31] = 'Bureaucrat'
    profs_en[32] = 'Celebrity'
    profs_en[33] = 'Twitter Phenomenon'
    profs_en[34] = 'Producer'
    profs_en[35] = 'Athlete'
    profs_en[36] = 'Commentator'
    profs_en[37] = 'CHP'
    profs_en[38] = 'TV Series actor'
    profs_en[39] = 'Businessman'
    profs_en[40] = 'AKP'
    profs_en[41] = 'Academician'
    profs_en[42] = 'Musician'
    profs_en[43] = 'Politician'
    profs_en[44] = 'TV host'
    profs_en[45] = 'Author'
    profs_en[46] = 'Artist'
    profs_en[47] = 'Columnist'
    profs_en[48] = 'MP'
    profs_en[49] = 'Journalist'
    
    for i in range(len(profs)):
        df.profs = df.profs.replace(profs[i],profs_en[i],regex=True)
    df.to_csv("data/TR-tweeps-En.csv",encoding='utf-8',index=False)
    """
    twcnt = [len(tweepset) for tweepset in tweeps]
    texts = []
    for twpset in tweeps[twcnt.index(6):]:
        text = u''
        for i,twp in enumerate(twpset):
            #twp = '<a href="http://twitter.com/'+twp[1:]+'">'+ twp +'</a>'
            text+= ' '+ twp if (i+1) % 10 != 0 else '<br>'+twp
        texts.append(text)

    data = Data([Bar(
            x=twcnt[twcnt.index(6):],
            y=profs_en[twcnt.index(6):],#profs[twcnt.index(6):],
            text=texts,
            orientation='h',
            marker=Marker(color='rgb(201,148,199)')
            )])
    layout = Layout(title="Turkish Newsmaker-Commentators by Profession (curated by nediyor.com)",
                    margin=Margin(l=130))
    fig = Figure(data=data, layout=layout)
    py.iplot(fig,filename="Nediyor.com Commentators by Profession")


def get_party_representation():
    """ Plot Twitter Usage vs MP counts """
    import pandas as pd
    import plotly.plotly as py
    from plotly.graph_objs import *

    #http://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.dagilim
    parties = {'AKP':312, 'CHP':125, 'HDP':27, 'MHP':52, 'Independent':13}
    mpc = sum(parties.values())
    df = pd.read_csv('data/TR-tweeps-En.csv',encoding='utf-8')
    
    # both returns 167, so each MP belongs to one and only one party
    # df[df.profs.str.contains('MP')].shape[0]
    # sum(df[df.profs.str.contains(p)].shape[0] for p in parties.keys())
    
    # Parties' newsworthy tweet counts normalized by MP counts
    perMP = {}
    for p,cnt in parties.iteritems():
        perMP[p] = df[df.profs.str.contains(p)].fcnt.sum()/float(cnt)

    # Parties' newsworthy tweet counts normalized by MPs with Twitter accounts
    perTweep = {}
    for p,cnt in parties.iteritems():
        perTweep[p] = df[df.profs.str.contains(p)].fcnt.sum()/float(df[df.profs.str.contains(p)].shape[0])
    
    
    x  = ['AKP', 'CHP', 'MHP', 'HDP','Independent']
    y1 = [int((perMP[p] * 100) + 0.5) / 100.0 for p in x]
    y2 = [int((perTweep[p] * 100) + 0.5) / 100.0 for p in x]
    
    texts = []
    for p in x:
        twpset = df[df.profs.str.contains(p)].twhandle.tolist()
        text = u''
        for i,twp in enumerate(twpset):
            #twp = '<a href="http://twitter.com/'+twp[1:]+'">'+ twp +'</a>'
            text+= ' '+ twp if (i+1) % 10 != 0 else '<br>'+twp
        texts.append(text)
        
    trace1 = Bar(x=x, y=y1, name='by their MP counts', text = texts)
    trace2 = Bar(x=x, y=y2, name='by curated tweep counts')
    data = Data([trace1, trace2])
    layout = Layout(
        title="Newsworthy Tweet Counts of Turkish Parties Normalized",
        barmode='group',
        legend=Legend(x=0, y=1,traceorder='normal'),
        yaxis=YAxis(title='Number of newsworthy tweets per MP'),
        annotations=Annotations([
            Annotation(
            text='Code and datasets are available on <a href="https://github.com/oztalha/News-Commentary-Tweets-of-Elites">github.com/oztalha</a><br>'\
                 'Two years of curated tweets are scraped from <a href="http://nediyor.com/">nediyor.com</a>',
            showarrow=False,
            x=0.01,
            y=0.9,
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            align='left'
            ),
        ]))
    fig = Figure(data=data, layout=layout)
    py.iplot(fig, filename='Newsworthy Tweet Counts of Turkish Parties')
    
    #tweep/mp ratio
    y = [df[df.profs.str.contains(p)].shape[0] for p in x]
