# -*- coding: utf-8 -*-
"""
@author: Talha Oz
"""
import pandas as pd
from gensim import corpora, models
from nltk.corpus import stopwords
import nltk
import snowballstemmer
import re

df = pd.read_csv('data/TR-news.csv',usecols=['dt','title','newstxt'],parse_dates=[0])
documents = df.newstxt.tolist()

stoplist = stopwords.words('turkish')
stoplist = [word for word in stoplist]
stoplist.extend("active number yes titlesection bootstrap tabtitle tboot tab tabcontent contentsection nin".split())

#stemmer = snowballstemmer.TurkishStemmer()
texts=[]
for doc in documents:
    doc = re.sub('[!"#%\'()*+,-./:;<=>?@\[\]^_`{|}~1234567890’”“′‘\\\]',' ', doc).split()
    #doc = stemmer.stemWords(doc)
    text= [w.strip() for w in doc if len(w.strip())>=3 and w.strip() not in stoplist]
    texts.append(text)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
n_topics = 10
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics, passes=5, alpha='auto')
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics, onepass=False, power_iters=5)

for i in range(0, n_topics):
    terms = [term[1] for term in lsi.show_topic(i, 20)]
    print ("#" + str(i) + ": "+ ", ".join(terms))

for i in range(0, n_topics):
    terms = [term[1] for term in lda.show_topic(i, 20)]
    print ("#" + str(i) + ": "+ ", ".join(terms))
