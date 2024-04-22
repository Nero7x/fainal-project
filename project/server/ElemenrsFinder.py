import string
import re
import nltk
import numpy as np
import pandas as pd

class ElementsFinder:

    keywords = {}
    punct = string.punctuation
    def get_unused_puncs(kws):
        puncs = list(ElementsFinder.punct)
        for kw in kws:
            for c in kw:
                if c in puncs:
                    puncs.remove(c)
        puncs = re.compile('[' + ''.join(puncs) + ']')
        return puncs
    
   


    def clean_tags_and_titles(train):
        train['Tags'] = train['Tags'].str.lower().str.split(' ')
        known_kws = np.hstack(train['Tags'].values)
        known_kws = np.unique(known_kws)

        unused_puncs = ElementsFinder.get_unused_puncs(known_kws)

        stopwords = nltk.corpus.stopwords.words('english')

        train['Title'] = train['Title'].str.lower().replace(unused_puncs, '').str.split(' ').map(lambda x: list(set(x).difference(stopwords)))
        return train



    def keyword_existence(tag_kws, title_kws):
        index = 0
        if type(tag_kws) == float or type(title_kws) == float:
            return
        print(set(title_kws).difference(tag_kws))
        for kw in set(title_kws).difference(tag_kws):
            ElementsFinder.keywords.setdefault(kw, 0)
            ElementsFinder.keywords.setdefault[kw].setdefault('title', 0)
            ElementsFinder.keywords.setdefault[kw]['title'] += 1
        print("second")
        index = 0
        for kw in set(title_kws).intersection(tag_kws):
            print(index)
            ElementsFinder.keywords.setdefault.setdefault(kw, {})
            ElementsFinder.keywords.setdefault[kw].setdefault('both', 0)
            ElementsFinder.keywords.setdefault[kw]['both'] += 1
        print("Third")
        index = 0
        for kw in set(tag_kws).difference(title_kws):
            print(index)
            ElementsFinder.keywords.setdefault.setdefault(kw, {})
            ElementsFinder.keywords.setdefault[kw].setdefault('tag', 0)
            ElementsFinder.keywords.setdefault[kw]['tag'] += 1


    def check_keywords(tag_kws, title_kws):
        for kw in tag_kws:
            if '-' in kw:
                kw_new = kw.replace('-', ' ')
                if set(kw_new).issubset(title_kws):
                    ElementsFinder.keywords.setdefault(kw, {})
                    ElementsFinder.keywords[kw].setdefault('both', 0)
                    ElementsFinder.keywords[kw]['both'] += 1



    def calculate_scores(keywords, train):
        n = len(train.index)
        removeKeys = []
        for kw in keywords.keys():
            keywords[kw].setdefault('title', 0)
            keywords[kw].setdefault('both', 0)
            keywords[kw].setdefault('tag', 0)
            total_tag = keywords[kw]['both'] + keywords[kw]['tag']
            total_title = keywords[kw]['both'] + keywords[kw]['title']
        
            if total_tag == 0:
                removeKeys.append(kw)
            elif total_title == 0:
                removeKeys.append(kw)
            else:
                p = keywords[kw]['both'] / (keywords[kw]['both'] + keywords[kw]['title']) 
                t1 = keywords[kw]['both'] / n * (keywords[kw]['both'] + keywords[kw]['title']) 
                t2 = keywords[kw]['both'] * np.log(n / total_title) 
            
                if t1 <= 1: 
                    removeKeys.append(kw)

        return removeKeys
    


    def nb_classify(test, keywords):
        unused_puncs = ElementsFinder.get_unused_puncs(keywords.keys())
        stopwords = nltk.corpus.stopwords.words('english')
        test['Title'] = test['Title'].str.lower().replace(unused_puncs, '').str.split(' ').map(lambda x: list(set(x).difference(stopwords)))

        pred = test[['Id']]
        pred['Tags'] = pd.Series(test['Title'].map(lambda x: ElementsFinder.decision_rule(x, keywords, stopwords)).map(lambda x: ' '.join(x)))

        return pred



    def decision_rule(title_hws, keywords, stopwords):
        nb_scores = {}
        ti_scores = {}
        for hw in set(title_hws).intersection(keywords.keys()):
            nb_scores[hw] = keywords[hw]['p']
            ti_scores[hw] = keywords[hw]['ti']

        for hw in filter(lambda x: '-' in x, keywords.keys()):
            hw_new = set(hw.replace('-', ' ').split()).difference(stopwords)
            if hw_new.issubset(title_hws):
                nb_scores[hw] = keywords[hw]['p']
                ti_scores[hw] = keywords[hw]['ti']

        hws_to_tag = []
        for hw in sorted(nb_scores, key=nb_scores.get, reverse=True):
            if nb_scores[hw] >= 0.5:
                hws_to_tag.append(hw)

        for hw in sorted(ti_scores, key=ti_scores.get, reverse=True):
            if hw not in hws_to_tag:
                hws_to_tag.append(hw)
                break

        if len(hws_to_tag) == 0:
            hws_to_tag.append('unknown')

        return hws_to_tag