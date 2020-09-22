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
    summaries = []

    for url in urls:
        summary = finalise(url)
        summaries.append(summary)

    for num in range(0,5):
        print(titles[num] +'\n')
        print(summaries[num] + '\n')
    
    # pool = multiprocessing.Pool()
    # summaries = [pool.map(finalise, urls)]
    # pool.close()
    # pool.join()
    # summaries = summaries[0]

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
