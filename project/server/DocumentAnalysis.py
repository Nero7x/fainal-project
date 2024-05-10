import io
from PyPDF2 import PdfReader 
import os
import tempfile
import spacy
import fitz
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

def dataInitialization(file,file_extension):
    texts = ""
    if file_extension == ".txt":
        text = file.read().decode('utf-8') 
        texts = nltk.sent_tokenize(text)

    elif file_extension ==".pdf":
        reader = PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        texts = nltk.sent_tokenize(text)
    nlp = spacy.load('en_core_web_sm')

    results = {}

    for text in texts:
        doc = nlp(text)
        actor = EF.ElementsFinder.findActor(doc)
        usecase = EF.ElementsFinder.findUsecase(doc,actor)
        ucr = RF.RelationshipFinder.findUsecaseRelationship(doc, actor)
        clas = EF.ElementsFinder.findClass(doc)
        attr = EF.ElementsFinder.findAttributes(doc)
        method = EF.ElementsFinder.findMethod(doc,actor)
        #cr = RF.RelationshipFinder.findClassRleationship(doc)

        results[text] = {
        'actors': actor,
        'usecases': usecase,
        'usecase relationship': ucr,
        'class': clas,
        'attributes': attr,
        'method' : method,
        }

    for i,result in enumerate(results):
        print(f"{i}- {result}: {results[result]}")


if __name__ == '__main__':
    document = "req.txt"
    dataInitialization(document)


