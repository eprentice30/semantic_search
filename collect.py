import re
import requests
import pandas as pd
import numpy as np
import string
from string import punctuation
from pymongo import MongoClient

import matplotlib.pyplot as plt

import seaborn as sns

from IPython.display import display
from scipy import stats
from sklearn.model_selection import train_test_split

np.random.seed(42)

import sys
argList = sys.argv

from sys import stdout
from time import sleep

page_input = str(argList[1]) #making sure the first argument is a string
levels = int(argList[2]) #making sure the second argument is an integer



def search_category(category):
    """"Returns the json of a page for a specific category"""
    
    category = re.sub('\s', '+', category)
    query = 'http://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category%3A+{}&cmlimit=max'.format(category)
    query_request = requests.get(query)
    return query_request.json()

def change_to_df(category):
    """"Returns the page contents as a DF"""
    
    title = search_category(category)['query']['categorymembers']
    df = pd.DataFrame(title)
    return df

def check_if_any_sub_categories(category):
    """"Returns true if there are subcategories"""
    
    df = change_to_df(category)
    if df[df['title'].str.contains('Category:')].any()[0]:
        return True
    else:
        return False

def strip_punctuation(s):
    """"Removes all unnecessary punctuation"""
    return ''.join(c for c in s if c not in punctuation)

def striphtml(data):
    """Removes all html"""
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_page_contents(pageid):
    """Returns cleaned page contents"""
    
    query = 'http://en.wikipedia.org/w/api.php?action=query&prop=extracts&\
             rvprop=content&rvsection=0&format=json&pageids={}'.format(pageid)
    
    my_request = requests.get(query).json()
    
    no_html_string = striphtml(my_request['query']['pages'][str(pageid)]['extract']).replace('\n', ' ')
    
    return strip_punctuation(no_html_string)

def search_wiki(category, pages, set_of_categories, levels):

    levels -= 1
    df = change_to_df(category)
    if levels != -1: #to make sure we don't go deeper than specified
    
        if check_if_any_sub_categories(category):
            if category not in set_of_categories: #to make sure we don't repeat pages
                set_of_categories.add(category)
                for i in range(len(df)):
                    index = df['pageid'][i]
            
                    if i%10 == 0:
                        #print the category for every 10 pages gathered to make sure it's working
                        stdout.write(category + ' ')
                        stdout.flush()
                        

                    if 'Category:' in df['title'][i]:
                        category = df['title'][i]
                        category = category.replace('Category:','') #stripping category from the name of the title
                        search_wiki(category, pages, set_of_categories, levels) #recursion
                
                    else:
                        page = get_page_contents(index)
                        pages.update({index:{'page_contents': page,
                            'category': category,
                            'page_title': df['title'][i]}})

        
        else: 
            for i in range(len(df)):
                if i%10 == 0:
                    stdout.write(category + ' ')
                    stdout.flush()
                index = df['pageid'][i]
                page = get_page_contents(index)
                pages.update({index:{'page_contents': page,
                            'category': category,
                            'page_title': df['title'][i]}})
    
    client = MongoClient('54.245.184.134', 27016)
    db_ref = client.wikipedia_database
    coll_ref = db_ref.wikipedia_collection
    
    for keys in pages.keys():
        #passing the dictionary into the MongoDB
        try:
            coll_ref.insert_one(pages[keys])
        except:
            #if the page is already in the collection
            pass

    return pages


pages = {}
set_of_categories = set()

p = search_wiki(page_input, pages, set_of_categories, levels)