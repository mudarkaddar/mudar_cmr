from django.shortcuts import render
from django.http import JsonResponse
import json
from nltk.stem.isri import ISRIStemmer
from rouge import Rouge
import arabic_reshaper
import networkx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from  matplotlib import *
from scipy.sparse.linalg import svds
from .farwell import *
import requests,urllib3
from bs4 import BeautifulSoup

ROUGE=Rouge()

# Create your views here.



def evaluate(request):
    
    tr1 = request.GET.get('trone')
    tr2 = request.GET.get('trtwo')
    result = request.GET.get('result')
    
    # if(result != '1'):
    #     return render(request, 'evaluate.html')
    # print(tr1)
    # print(tr2)
 
    return render(request, 'evaluate.html',{'message':tr1})


# def evaluate(request):
#     if request.method == 'GET':
#         trone = request.GET.get('trone', '')
#         trtwo = request.GET.get('trtwo', '')

#         # Perform your evaluation logic here
        
#         result = {'message': trone+trtwo}

#         return JsonResponse(result)

#     return render(request, 'evaluate.html')





def lsa(doc ,num_sentences = 2,num_topics = 3,sv_threshold = 0.5):
    sum_texts=''
    for docy in doc:
        snt =doc_to_sent(docy)
        norm_snt=normalize_all_document(snt)
        dt_matrix ,td_matrix , vocab=Tfidf_Vectorizer (norm_snt)
        summarized_text=Latent_Semantic_Analysis(td_matrix,snt,num_sentences ,num_topics,sv_threshold )+'\n'
        sum_texts=sum_texts+summarized_text
    return  {'message': sum_texts}






def function1_logic(a):
    print('Button 1 clicked')
    return {'message': a}

def function2_logic(b):
    print('Button 2 clicked')
    return {'message': b}

def function3_logic(c):
    print('Button 3 clicked')
    return {'message': c}

def function4_logic(rt):

    articles=[]
    no = int(rt.GET.get('no')) 
    article_url = rt.GET.get('article_url')  



    i=no
    
    print(i)
    print(article_url)

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

    elif website=="https://imn.iq/" :
        headlines = soup.find_all('a',{"class":"img-cont"})

    elif website=="https://www.bbc.com/arabic" :
        headlines = soup.find_all('a',{"class":"focusIndicatorDisplayInlineBlock"})
        
    
    if(i<=len(headlines)):
        samir=[]
        for item in headlines[:i]:

            
            samir.append(website.replace('/arabic','')+item.get('href').replace(website,""))

            # samir.append(website+item.get('href'))

        for url in samir:
            paragraphs=""
            http = urllib3.PoolManager()
            

            html = http.request('GET', url)

            html2=html.data

            htmlParse = BeautifulSoup(html2, 'html.parser')

            for para in htmlParse.find_all("p"):
                # if '::post' in para.get_text():
                    # continue
                paragraphs=paragraphs+para.get_text()
            
            articles.append(paragraphs)
        return articles
            
      
def index(request):
    print("1")
    response_data = {}
    action = request.GET.get('action')

    print("2")
    
    if action =='f4':
        
        arcs_list=function4_logic(request)
        print(arcs_list)
        # tts='\n**************************************************************************\n'.join(arcs_list)


        response_data={'message':arcs_list,'samira':"\nhello from the other side"}
    
    elif action == 'f1':
        response_data = lsa(arcs_list,num_sentences = 2,num_topics = 3,sv_threshold = 3) 
        
    elif action == 'f2':
        response_data = lsa(arcs_list)

    elif action == 'f3':
        response_data = lsa(arcs_list)
        
    print(response_data)
 
    return render(request, 'index.html', response_data)
