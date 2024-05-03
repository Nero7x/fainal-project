import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk as nltk
import string
from server import ElemenrsFinder as EF
from server import ReletionshipFinder as RF

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
         "The system sends a notification to the user.",
         "The user can change their password at any time.",
         "The system automatically logs out after a period of inactivity for 15 minutes.",
         "The admin can add or delete users from the system.",
         "The system stores all user data securely.",
         "The user can recover their password using their email address.",
         "The system verifies the user's email address before creating an account.",
         "The admin can view usage statistics for all users.",
         "The user can upload and download files.",
         "The system encrypts all sensitive data.",
         "The admin can reset a user's password.",
         "The user can update their profile picture.",
         "The system maintains a log of all user activity.",
         "The user can search for other users.",
         "The system provides two-factor authentication for added security.",
         "The admin can suspend or reactivate user accounts.",
         "The user can send messages to other users.",
         "The system sends a confirmation email after successful registration."]


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

    for token in doc:
        if token.pos_ == 'VERB':
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
            if token.text not in nouns_with_verbs:
                nouns_without_verbs.append(token.text)

        actor = EF.ElementsFinder.findActor(doc)
        usecase = EF.ElementsFinder.findUsecase(doc,actor)
        ucr = RF.RelationshipFinder.findUsecaseRelationship(doc)
        clas = EF.ElementsFinder.findClass(doc)
        attr = EF.ElementsFinder.findAttributes(doc)
        method = EF.ElementsFinder.findMethod(doc,actor)

    # تخزين المخرجات في القاموس
        output_dict[text] = {
        #'actors 1': nouns_with_verbs,
        'actors 2': actor,
        #'usecases 1': verbs_with_nouns,
        'usecases 2': usecase,
        #'usecase relationship 1': noun_verb_relations,
        'usecase relationship 2': ucr,
        #'class 1': nouns_with_verbs,
        'class 2': clas,
        #'attributes 1': nouns_without_verbs,
        'attributes 2': attr,
        #'relation': verbs_without_nouns,
        'method' : method,
        }

print(output_dict)



