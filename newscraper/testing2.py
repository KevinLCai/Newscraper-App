#Import necessary modules and functions
import requests
from bs4 import BeautifulSoup
import webbrowser
from collections import Counter
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import concurrent.futures
import time
from multiprocessing import Pool

#Text summariser using extractive summarisation:
#Turn url into the article's text - NEED TO REMOVE IRRELEVANT STUFF

urls = ['https://www.bbc.co.uk/news/health-54163226', 'https://www.bbc.co.uk/news/uk-51768274', 'https://www.bbc.co.uk/news/uk-54165870', 'https://www.bbc.co.uk/news/uk-northern-ireland-53988050', 'https://www.bbc.co.uk/news/disability-53863013']

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

        #print(tokens)
        #print(sents)

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

#USE MULTIPROCESSING HERE

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(finalise, urls) 
        summaries = []
        for result in results:
            summaries.append(result)
        if summaries != None:
            final_summaries = summaries
            print(final_summaries)
