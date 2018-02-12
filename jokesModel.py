import pickle
import time

import numpy as np
import gensim
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity


from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import download


with open ('./kid_joke_q.txt', 'rb') as fp:
    kid_qs = pickle.load(fp)

with open ('./kid_joke_a.txt', 'rb') as fp:
    kid_as = pickle.load(fp)

with open ('./kids_q_corpus.pickle', 'rb') as fp:
    kids_q_corpus = pickle.load(fp)
    

tfidf = TfidfModel.load('./jokes_tfidf.model')
lsi = LsiModel.load('./jokes_lsi.model')


download('stopwords')
stop_words = stopwords.words('english')
dictionary = corpora.Dictionary.load('./all_jokes_dictionary.model')


def preprocess(text):
    text = text.lower()
    doc = word_tokenize(text)
    doc = [word for word in doc if word not in stop_words]
    doc = [word for word in doc if word.isalpha()]
    return doc



def findMatchesInJokes(text="What's blue all over? ", topNum=3, corpus=kids_q_corpus, texts=kid_qs):
    start_time = time.time()
    test_text = text
    #test_text = texts[0]
    test_text
    processed_test_text = preprocess(test_text)
    test_text_gensim = dictionary.doc2bow(processed_test_text)
    test_text_tfidf = tfidf[[test_text_gensim]]
    if len(test_text_tfidf[0]) ==0 : 
        print("Not enough features, try again. ")
        return []
    # the slow steps
    test_text_lsi_index = MatrixSimilarity(lsi[test_text_tfidf])
    corpus_tfidf = [dictionary.doc2bow(doc) for doc in corpus]
    kids_test_text_sims = np.array([test_text_lsi_index[lsi[corpus_tfidf[i]]] 
                           for i in range(len(corpus))])
    kids_r = np.argsort(kids_test_text_sims.flatten())[-topNum:]
    kids_r = list(reversed(kids_r))
    for ii in range(len(kids_r)):
        print(texts[kids_r[ii]])
        
    print("--- %s seconds ---" % (time.time() - start_time))
    return kids_r



#rs = findMatchesInJokes(text="what's fat, yo mama? ", topNum=10, corpus=kids_q_corpus, texts=kid_qs)

#rs = findMatchesInJokes(text="what's fat, yo mama? ")


def getMatchingJokesJSON(text):
    rs = findMatchesInJokes(text="what's fat, yo mama? ")
    if (len(rs) ==0):
        return {'message': 'no match'}
    
    jokes = {}
    counter = 1
    for i in rs:
        jokes[counter] = {}
        jokes[counter]['q'] = kid_qs[i]
        jokes[counter]['a'] = kid_as[i]
        counter = counter +1
    return jokes
