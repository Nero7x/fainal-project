import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk as nltk
import string

doc = "./client/nfr.csv"
req_data = pd.read_csv(doc, delimiter=':', nrows=5, header=None)
req_data.columns= ['type', 'req']

pd.set_option('display.max_colwidth', 100)
print(req_data.head(5))

def remove_punct(text):
    text_nopuct = "".join([char for char in text if char not in string.punctuation])
    return text_nopuct
    

df=req_data.copy()

df['req_nopunct'] = df['req'].apply(lambda x: remove_punct(x.lower()))
print(df.head(5))