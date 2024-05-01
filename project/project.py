import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk as nltk
import string

#doc = "./client/nfr.csv"
#req_data = pd.read_csv(doc, delimiter=':', nrows=5, header=None)
#req_data.columns= ['type', 'req']

#pd.set_option('display.max_colwidth', 100)
#print(req_data.head(5))

#def remove_punct(text):
    #text_nopuct = "".join([char for char in text if char not in string.punctuation])
    #return text_nopuct
    

#df=req_data.copy()

#df['req_nopunct'] = df['req'].apply(lambda x: remove_punct(x.lower()))
#print(df.head(5))

import spacy

# تحميل النموذج اللغوي
nlp = spacy.load('en_core_web_sm')

# الجمل التي نريد تحليلها
texts = ["The user logs in to the system using their username and password.",
         "The admin updates the user's profile.",
         "The system sends a notification to the user."]

# قاموس لتخزين النتائج
output_dict = {}


for text in texts:

    # تحليل النص
    doc = nlp(text)

    # استخراج الأفعال والأسماء والعلاقات بينهم
    nouns_with_verbs = []
    nouns_without_verbs = []
    verbs_with_nouns = []
    verbs_without_nouns = []
    noun_verb_relations = []

    verbs = []
    nouns = []
    for token in doc:
        if token.pos_ == 'VERB':
            verbs.append(token.text)
            has_noun = False
            for child in token.children:
                if child.pos_ == 'NOUN':
                    nouns_with_verbs.append(child.text)
                    verbs_with_nouns.append(token.text)
                    noun_verb_relations.append(f'Association({child.text} --- {token.text})')
                    has_noun = True
            if not has_noun:
                verbs_without_nouns.append(token.text)
        elif token.pos_ == 'NOUN':

            nouns.append(token.text)

            if token.text not in nouns_with_verbs:
                nouns_without_verbs.append(token.text)

    # تخزين المخرجات في القاموس
        output_dict[text] = {
        'actors': nouns_with_verbs,
        'usecases': verbs_with_nouns,
        'usecase relationship': noun_verb_relations,
        'class': nouns_with_verbs,
        'attributes': nouns_without_verbs,
        'relation': verbs_without_nouns
        }

print(output_dict)



