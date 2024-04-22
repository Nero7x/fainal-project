import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk as nltk

class NLPmodel:
    def read_data():
        doc = "./client/nfr.csv"
        req_data = pd.read_csv(doc, delimiter=':', nrows=5, header=None)
        req_data.columns= ['type', 'req']
        print(req_data.head(5))

        df=req_data.copy()
        df['req_nopunct'] = df['req'].apply(lambda x: Normalization().remove_punct(doc))
        df.head()
        

    
