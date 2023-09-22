from django.shortcuts import render
import json
from nltk.stem.isri import ISRIStemmer
import numpy as np
import nltk
import re
import pandas as pd
import math
import csv
from rouge import Rouge
import arabic_reshaper
import networkx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from  matplotlib import *
from scipy.sparse.linalg import svds
# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from .farwell import *
import requests,urllib3
from bs4 import BeautifulSoup
from .forms import EvaluationForm


ROUGE=Rouge()

# Create your views here.



def evaluate(request):
    return render(request, 'evaluate.html')


def lsa(doc ,num_sentences = 4,num_topics = 1,sv_threshold = 0.5):
    snt =doc_to_sent(doc)
    norm_snt=normalize_all_document(snt)
    print(norm_snt)
    dt_matrix ,td_matrix , vocab=Tfidf_Vectorizer (norm_snt)
    print(td_matrix)
    summarized_text=Latent_Semantic_Analysis(td_matrix,snt,num_sentences ,num_topics,sv_threshold )
    return {'message': summarized_text}

def function2_logic(b):
    print('Button 2 clicked')
    return {'message': b}

def function3_logic(c):
    print('Button 3 clicked')
    return {'message': c}

def function4_logic(rt):
    
    no = int(rt.GET.get('no')) 
    article_url = rt.GET.get('article_url')  
    
    i=no
    print(i)
    website = article_url
    r = requests.get(website)
    r_html = r.text
    soup = BeautifulSoup(r_html, features="html.parser")
    if website=="https://www.skynewsarabia.com/":
        headlines = soup.find_all('a',{'class':'comp_1_item_inner_cont'})
    elif website=="https://alwatan.sy/" :
        headlines = soup.find_all('a',{'class':'all-over-thumb-link'})
    elif website=="https://www.almayadeen.net/" :
        headlines = soup.find_all('a',{"class":"media-figure"})
    elif  website == "https://www.aljazeera.net/":
        headlines = soup.find_all('a',{"class":"u-clickable-card__link"}) 
    elif website=="https://imn.iq/" :
      headlines = soup.find_all('a',{"class":"img-cont"})
    elif website=="https://www.bbc.com/arabic" :
      headlines = soup.find_all('a',{"class":"focusIndicatorDisplayInlineBlock"})
        
    samir=[]
    
    if(i==0):
        for item in headlines:
            
            samir.append(website.replace('/arabic','')+item.get('href').replace(website,""))
            

        for url in samir:
            http = urllib3.PoolManager()

            html = http.request('GET', url)

            html2=html.data

            htmlParse = BeautifulSoup(html2, 'html.parser')
            articles=""

            for para in htmlParse.find_all("p"):
                articles=articles+(para.get_text())+'***********************************************************************************************'
        return articles
    else:
            item=headlines[i-1]
            url=website.replace('/arabic','')+item.get('href').replace(website,"")
            http = urllib3.PoolManager()

            html = http.request('GET', url)

            html2=html.data

            htmlParse = BeautifulSoup(html2, 'html.parser')
            articles = ""
            for para in htmlParse.find_all("p"):
                
                articles = articles+para.get_text()
            print(articles)
            return articles

            
      


def index(request):
    print("1")
    response_data = {}
    
    action = request.GET.get('action')
    tts = request.GET.get('textarea')
    print("2")
    
    if action =='f4':
        
        tts=function4_logic(request)
        response_data={'message':tts}
        print("3")
    
    elif action == 'f1':
        response_data = lsa(tts)
        print("4")
        
    elif action == 'f2':
        response_data = function2_logic(tts)

    elif action == 'f3':
        response_data = function3_logic(tts)

        
    print(response_data)
 
    return render(request, 'index.html', response_data)





