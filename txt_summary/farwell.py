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
from nltk.stem import PorterStemmer
import pyarabic.araby as araby
from nltk.corpus import stopwords
ROUGE=Rouge()

stopwords=set (stopwords.words('arabic'))
# data={}
# with open('txt_summary\list.txt','r',encoding='utf-8') as stopwords_file:
#     data = stopwords_file.read()
#     data = set(data.replace('\n', ' ').split("."))
    

def remove_urls(article,work=1):
    if(work==1):
        for p in re.findall("https?://[\w\./]+", article):
            article = re.sub(p,"", article)
        for p in re.findall("www\.[\./]+",article):
            article = re.sub(p,"", article)
    return article


def remove_RepetitionCharacter(article,work=1):
    if(work==1):

        words = article.split()
        result = list()
        word_list=[]
        for word in words:
            stack=[]
            for p in word:
                if len(stack):
                    x=stack.pop()
                    if (x!=p):
                        stack.append(x)
                        stack.append(p)
                    else :
                        stack.append(x)
                else :
                    stack.append(p)
            w=''.join(stack)
            word_list.append(w)
    return ' '.join(word_list)




def lemmatization(artical,work=1):
    if(work==1):

        words = artical.split()
        result = list()
        stemmer = ISRIStemmer()
        for word in words:
            if(re.search(r'(كور|كرو)',word)):
                result.append(word)
                continue
            word = stemmer.norm(word, num=1)
            if not word in stemmer.stop_words :
                word = stemmer.pre32(word)
                word = stemmer.suf32(word)
                word = stemmer.waw(word)
                word = stemmer.norm(word, num=2)
            result.append(word)
    return ' '.join(result)



def Character_Standardization(artical ,work=1):
    if (work==1):
        a='أإآ'
        b='ئؤ'
        for char in a :
            artical = artical.replace(char,"ا")
        for char in b :
             artical = artical.replace(char,"ء")
        artical = artical.replace("ة","ت")
    return artical




def remove_stopword(tweet, work=1):
    if(work==1):
        words = tweet.split()
        for word in words:
            if  word in stopwords:
                tweet = re.sub(word,"", tweet)
    return tweet



def remove_multiple_spaces(artical,work=1):
    if(work==1):
        artical = re.sub(r" +"," ", artical)
    return artical



def non_arabic (artical ,work=1):
    if work==1:
        for p in re.findall('[A-Za-z]+', artical):
            artical = re.sub(p,"", artical)
    return artical


def preprocess(artical, flags=[1,1,1,1,1,1,1,1]):
    artical= str(artical)
    artical = remove_urls(artical, flags[0])

    artical = remove_RepetitionCharacter(artical,flags[1])

    artical = remove_stopword(artical, flags[2])
    artical = lemmatization(artical,flags[3])
    artical = Character_Standardization(artical,flags[4])
    artical = remove_multiple_spaces(artical,flags[5])
    artical= non_arabic(artical ,flags[5])
    return artical



def normalize_document(doc):
    doc =preprocess(doc, flags=[1,1,1,1,1,1,1,1])
    return doc



def normalize_all_document(sentences):
    normalize_corpus = np.vectorize(normalize_document)
    return normalize_corpus(sentences)



def Tfidf_Vectorizer (norm_sentences):
    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    print("tv: ",tv)
    dt_matrix = tv.fit_transform(norm_sentences)
    dt_matrix = dt_matrix.toarray()
    vocab = tv.get_feature_names_out()
    td_matrix = dt_matrix.T
    return dt_matrix ,td_matrix , vocab


def low_rank_svd(matrix, singular_count):
    print(min(matrix.shape))
    u, s, vt = svds(matrix, k=int(singular_count))
    return u, s, vt


def doc_to_sent(DOCUMENT):
    sent=[]
    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()
    DOCUMENTs = DOCUMENT.split(".")
    for doc in DOCUMENTs :
      sent.extend (araby.sentence_tokenize(doc))

    return  sent

def Latent_Semantic_Analysis(td_matrix,sentences,num_sentences = 8,num_topics = 3,sv_threshold = 0.5):
    

    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)
    term_topic_mat, singular_values, topic_document_mat = u, s, vt

    # remove singular values below threshold

    min_sigma_value = max(singular_values) * sv_threshold
    singular_values[singular_values < min_sigma_value] = 0
    salience_scores = np.sqrt(np.dot(np.square(singular_values),
                                 np.square(topic_document_mat)))
    top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
    top_sentence_indices.sort()
    return '\n'.join(np.array(sentences)[top_sentence_indices])




def networkx_dt_matrix(dt_matrix,num_sentences,sentences):
    
    similarity_matrix = np.matmul(dt_matrix, dt_matrix.T)

    np.round(similarity_matrix, 3)


    similarity_graph = networkx.from_numpy_array(similarity_matrix)

    plt.figure(figsize=(12, 6))
    networkx.draw_networkx(similarity_graph, node_color='lime')

    scores = networkx.pagerank(similarity_graph)

    ranked_sentences = sorted(((score, index) for index, score
                                            in scores.items()),
                              reverse=True)


    top_sentence_indices = [ranked_sentences[index][1]
                        for index in range(num_sentences)]
    top_sentence_indices.sort()

    return '\n'.join(np.array(sentences)[top_sentence_indices])

def sents_simi(doc,num_sentences=5):
    snt =doc_to_sent(doc)
    norm_snt=normalize_all_document(snt)
    dt_matrix ,td_matrix , vocab=Tfidf_Vectorizer (norm_snt)
    summarized_text=networkx_dt_matrix(dt_matrix,num_sentences,snt)
    return summarized_text

def sents_simi_list(docs ,num_sentences):
        
        sents_simi_all = np.vectorize(sents_simi)
        print(sents_simi_all(docs,num_sentences))
        return {'message':sents_simi_all(docs,num_sentences)}

def evaluate(candidate,reference):
    x=ROUGE.get_scores(candidate, reference)
    res1=x[0]['rouge-1']['f']
    res2=x[0]['rouge-2']['f']
    return res1,res2



def lsa(doc ,num_sentences = 7,num_topics = 3,sv_threshold = 0.5):
    snt =doc_to_sent(doc)
    norm_snt=normalize_all_document(snt)
    dt_matrix ,td_matrix , vocab=Tfidf_Vectorizer (norm_snt)
    summarized_text=Latent_Semantic_Analysis(td_matrix,snt,num_sentences ,num_topics,sv_threshold )
    return summarized_text



def lsa_list(docs ,num_sentences = 7,num_topics = 3,sv_threshold = 0.5):
    lsa_all = np.vectorize(lsa)
    print(lsa_all(docs,num_sentences,num_topics,sv_threshold))
    return {'message':lsa_all(docs,num_sentences,num_topics,sv_threshold)}