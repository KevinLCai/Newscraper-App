import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from .web_scraper import *
import time
import multiprocessing

import requests
from bs4 import BeautifulSoup
import webbrowser
from collections import Counter
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import concurrent.futures


def scrape1(catagory, array1):
    """FIND TITLES AND URLS"""
    if catagory == "us2020":
        catagory = 'election/us2020'
    #Store webpage data in variable called result
    result = requests.get(f'https://www.bbc.co.uk/news/{catagory}/')
    #print(result.status_code)
    #print(result.headers)
    #Store webpage content
    src = result.content
    #Convert into readable data
    soup = BeautifulSoup(src,'lxml')
    #Find all of the articles in the page (This is found by class)

    urls = []

    links = soup.find_all('a', class_ = 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    promo_story = soup.find('a', class_ ='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold gs-u-mt+ nw-o-link-split__anchor')
    links.insert(0, promo_story)

    
    def findLinks():
        """Find all of the links to articles and add them to a urls array"""
        while len(urls) <= 6:
            for link in links:
                try:
                    url = 'https://www.bbc.co.uk' + link.attrs['href']
                    if url not in urls and url.startswith('https://www.bbc.co.uk/news/') and ("/live/" not in url):
                        urls.append(url)
                except:
                    pass
    
    final_urls = []

    def findTitle():
        """Find title for each url-article"""
        
        while len(array1) < 5:
            for url in urls:
                try:
                    article = requests.get(url)
                    article = article.content
                    article = BeautifulSoup(article, 'lxml')
                    article_title = article.find('h1', class_ = 'story-body__h1').text
                    array1.append(article_title)
                    final_urls.append(url)
                except AttributeError:
                    try:
                        article_title = article.find('h1', class_ = 'vxp-media__headline').text
                        array1.append(article_title)
                        #print(article_title)
                    except AttributeError:
                        pass



    findLinks()
    #for url in urls[:5]:
        #print(url)
    findTitle()

    return [final_urls, array1]



    findLinks()
    #for url in urls[:5]:
        #print(url)
    findTitle()

    return [urls[:5], array1]

def tokenizer(s):
    tokens = []
    for word in s.split(' '):
        tokens.append(word.strip().lower())
    return tokens

def sent_tokenizer(s):
    sents = []
    for sent in s.split('.'):
        sents.append(sent.strip())
    return sents

#Count word occurences in document
def count_words(tokens):
    word_counts = {}
    for token in tokens:
        if token not in stop_words and token not in punctuation:
            if token not in word_counts.keys():
                word_counts[token] = 1
            else:
                word_counts[token] += 1
    return word_counts

#Count frequency of words
def word_freq_distribution(word_counts):
    freq_dist = {}
    max_freq = max(word_counts.values())
    for word in word_counts.keys():
        freq_dist[word] = (word_counts[word]/max_freq)
    return freq_dist

#Score sentences
def score_sentences(sents, freq_dist, max_len=40):
    sent_scores = {}
    for sent in sents:
        words = sent.split(' ')
        for word in words:
            if word.lower() in freq_dist.keys():
                if len(words) < max_len:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = freq_dist[word.lower()]
                    else:
                        sent_scores[sent] += freq_dist[word.lower()]
    return sent_scores

#Summarize using scores:
def summarize(sent_scores, k):
    top_sents = Counter(sent_scores)
    summary = ''
    scores = []

    top = top_sents.most_common(k)
    for t in top:
        summary += t[0].strip()+'. '
        scores.append((t[1], t[0]))
    return summary[:-1], scores

def finalise(url):
    try:
        array2 = []
        article = requests.get(url)
        article = article.content
        article = BeautifulSoup(article, 'lxml')
        paragraphs = article.find_all('p')

        string_concat = ''
        #Concatenate text into one string!
        for paragraph in paragraphs:
            string = paragraph.text
            string_concat += string + ' '
        text = string_concat

        text = text.replace("Share this withEmailFacebookMessengerMessengerTwitterPinterestWhatsAppLinkedInCopy this linkThese are external links and will open in a new window", "")
        text = text.replace("The BBC is not responsible for the content of external sites. Read about our approach to external linking.", "")
        text = text.replace("Share this with Email Facebook Messenger Messenger Twitter Pinterest WhatsApp LinkedIn", "")
        text = text.replace("Copy this link These are external links and will open in a new window", "")

        

        #Tokenise
        tokens = tokenizer(text)
        sents = sent_tokenizer(text)
        word_counts = count_words(tokens)
        word_counts
        freq_dist = word_freq_distribution(word_counts)
        freq_dist
        sent_scores = score_sentences(sents, freq_dist)
        sent_scores

        #Generate summary
        summary, summary_sent_scores = summarize(sent_scores, 3)
        #print(titles[number-1] + '\n')
        #print(summary)
        array2.append(summary)
        
        #print('\n')
    except IndexError:
        pass
    return summary


# titles = []
    
# info = scrape1('uk', titles)

# # #Multiprocessing to speed up scraping and summarising
# # with concurrent.futures.ProcessPoolExecutor() as executor:
# urls = info[0]
# titles = info[1]

# # print(urls)
# # print(titles)

# summaries = []

# for url in urls:
#     summary = finalise(url)
#     summaries.append(summary)

# for num in range(0,5):
#     print(titles[num] +'\n')
#     print(summaries[num] + '\n')

