import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .web_scraper import scrape


def index(request):
    return render(request, "newscraper/index.html")

def return_page(request, catagory):
    titles = []
    summaries = []
    info = scrape(catagory, titles, summaries)
    titles = info[0]
    summaries = info[1]
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