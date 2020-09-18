import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .web_scraper import *
import time
import multiprocessing

import requests
from bs4 import BeautifulSoup
import webbrowser
from collections import Counter
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import concurrent.futures

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

def index(request):
    return render(request, "newscraper/index.html")

def return_page(request, catagory):
    global final_summaries

    titles = []
    
    info = scrape1(catagory, titles)

    # #Multiprocessing to speed up scraping and summarising
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    urls = info[0]
    titles = info[1]
    
    pool = multiprocessing.Pool()
    summaries = [pool.map(finalise, urls)]
    pool.close()
    pool.join()
    summaries = summaries[0]

    # if final_summaries:
    return render(request, "newscraper/catagory.html", {
        'catagory' : catagory.title() if catagory != 'us2020' else 'US Election',
        'title1' : titles[0],
        'title2' : titles[1],
        'title3' : titles[2],
        'title4' : titles[3],
        'title5' : titles[4],
        'summary1' : summaries[0],
        'summary2' : summaries[1],
        'summary3' : summaries[2],
        'summary4' : summaries[3],
        'summary5' : summaries[4],
    })
