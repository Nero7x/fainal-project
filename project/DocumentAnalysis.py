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

nlp = spacy.load('en_core_web_sm')

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
         "The system sends a confirmation email after successful registration.",
         "The user can bookmark their favorite pages.",
         "The admin can manage roles and permissions of users.",
         "The system supports multiple languages.",
         "The user can view their activity history.",
         "The system performs regular backups of all data.",
         "The admin can generate reports based on user activity.",
         "The user can customize their user interface.",
         "The system provides a help section for new users.",
         "The admin can send global notifications to all users.",
         "The user can import and export data in various formats.",
         "The system provides an API for third-party integrations.",
         "The admin can perform bulk operations on multiple users at once.",
         "The user can opt-in or opt-out of email notifications.",
         "The system logs all errors and exceptions.",
         "The admin can schedule tasks to be performed automatically.",
         "The user can share their content with others.",
         "The system provides a search functionality with advanced filters.",
         "The admin can manage the system settings.",
         "The user can request support directly from the system.",
         "The system sends regular updates and patches.",]


output_dict = {}

for text in texts:

    doc = nlp(text)

    actor = EF.ElementsFinder.findActor(doc)
    usecase = EF.ElementsFinder.findUsecase(doc,actor)
    ucr = RF.RelationshipFinder.findUsecaseRelationship(doc, actor)
    clas = EF.ElementsFinder.findClass(doc)
    attr = EF.ElementsFinder.findAttributes(doc)
    method = EF.ElementsFinder.findMethod(doc,actor)
    #cr = RF.RelationshipFinder.findClassRleationship(doc)

    output_dict[text] = {
    #'actors 2': actor,
    'usecases 2': usecase,
    #'usecase relationship 2': ucr,
    #'class 2': clas,
    #'attributes 2': attr,
    #'method' : method,
    }

print(output_dict)





