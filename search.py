import re
import requests
import pandas as pd
import numpy as np
import string
from string import punctuation
from pymongo import MongoClient

import sys
argList = sys.argv

from sys import stdout

#### Taking the collected data from a MongoDB collection and turning it into a data frame ############
client = MongoClient('54.245.184.134', 27016)
db_ref = client.wikipedia_database
coll_ref = db_ref.wikipedia_collection

corpus_df = pd.DataFrame(list(coll_ref.find()))
################################################################################################

#################### Using SVD #################################################
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(min_df = 1, stop_words = 'english')

document_term_matrix_sps = tfidf_vectorizer.fit_transform(corpus_df.page_contents)

document_term_matrix_df = pd.DataFrame(document_term_matrix_sps.toarray(),
                                       index=corpus_df.index,
                                       columns=tfidf_vectorizer.get_feature_names())

from sklearn.decomposition import TruncatedSVD

n_components = 300 # ~37% of the variance can be explained by these components
SVD = TruncatedSVD(n_components)
component_names = ["component_"+str(i+1) for i in range(n_components)]

svd_matrix = SVD.fit_transform(document_term_matrix_df)
###################################################################################

################## Using cosine similarities to return top 5 articles ###################
search_term = argList[1]
search_term_vec = tfidf_vectorizer.transform([search_term])
search_term_lsa = SVD.transform(search_term_vec)

cosine_similarities = svd_matrix.dot(search_term_lsa.T).ravel()

indexes = cosine_similarities.argsort()[:-6:-1]

print('The top 5 articles relating to the search word are: ')
for i in indexes:
    print(corpus_df.iloc[i]['page_title'])

#################################################################################