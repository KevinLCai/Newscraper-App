#Import necessary modules and functions
import requests
from bs4 import BeautifulSoup
import webbrowser
from collections import Counter
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import concurrent.futures
import multiprocessing
import os



urls = ['https://www.bbc.co.uk/news/health-54163226', 'https://www.bbc.co.uk/news/uk-51768274', 'https://www.bbc.co.uk/news/uk-54165870', 'https://www.bbc.co.uk/news/uk-northern-ireland-53988050', 'https://www.bbc.co.uk/news/disability-53863013']


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
        while len(urls) <= 5:
            for link in links:
                try:
                    url = 'https://www.bbc.co.uk' + link.attrs['href']
                    if url not in urls and url.startswith('https://www.bbc.co.uk/news/') and ("/live/" not in url):
                        urls.append(url)
                except:
                    pass

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
                    #print(article_title)
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

    return [urls[:5], array1]

# def scrape2(urls, array2):
#     ###SUMMARISING PROCESS
#     #Tokenisers
#     def tokenizer(s):
#         tokens = []
#         for word in s.split(' '):
#             tokens.append(word.strip().lower())
#         return tokens

#     def sent_tokenizer(s):
#         sents = []
#         for sent in s.split('.'):
#             sents.append(sent.strip())
#         return sents

#     #Count word occurences in document
#     def count_words(tokens):
#         word_counts = {}
#         for token in tokens:
#             if token not in stop_words and token not in punctuation:
#                 if token not in word_counts.keys():
#                     word_counts[token] = 1
#                 else:
#                     word_counts[token] += 1
#         return word_counts

#     #Count frequency of words
#     def word_freq_distribution(word_counts):
#         freq_dist = {}
#         max_freq = max(word_counts.values())
#         for word in word_counts.keys():
#             freq_dist[word] = (word_counts[word]/max_freq)
#         return freq_dist

#     #Score sentences
#     def score_sentences(sents, freq_dist, max_len=40):
#         sent_scores = {}
#         for sent in sents:
#             words = sent.split(' ')
#             for word in words:
#                 if word.lower() in freq_dist.keys():
#                     if len(words) < max_len:
#                         if sent not in sent_scores.keys():
#                             sent_scores[sent] = freq_dist[word.lower()]
#                         else:
#                             sent_scores[sent] += freq_dist[word.lower()]
#         return sent_scores

#     #Summarize using scores:
#     def summarize(sent_scores, k):
#         top_sents = Counter(sent_scores)
#         summary = ''
#         scores = []

#         top = top_sents.most_common(k)
#         for t in top:
#             summary += t[0].strip()+'. '
#             scores.append((t[1], t[0]))
#         return summary[:-1], scores

#     #Text summariser using extractive summarisation:
#     #Turn url into the article's text - NEED TO REMOVE IRRELEVANT STUFF
#     def finalise(url):
#         try:
#             article = requests.get(url)
#             article = article.content
#             article = BeautifulSoup(article, 'lxml')
#             paragraphs = article.find_all('p')

#             string_concat = ''
#             #Concatenate text into one string!
#             for paragraph in paragraphs:
#                 string = paragraph.text
#                 string_concat += string + ' '
#             text = string_concat

#             text = text.replace("Share this withEmailFacebookMessengerMessengerTwitterPinterestWhatsAppLinkedInCopy this linkThese are external links and will open in a new window", "")
#             text = text.replace("The BBC is not responsible for the content of external sites. Read about our approach to external linking.", "")
#             text = text.replace("Share this with Email Facebook Messenger Messenger Twitter Pinterest WhatsApp LinkedIn", "")
#             text = text.replace("Copy this link These are external links and will open in a new window", "")

#             #Tokenise
#             tokens = tokenizer(text)
#             sents = sent_tokenizer(text)

#             #print(tokens)
#             #print(sents)

#             word_counts = count_words(tokens)
#             word_counts

#             freq_dist = word_freq_distribution(word_counts)
#             freq_dist

#             sent_scores = score_sentences(sents, freq_dist)
#             sent_scores

#             #Generate summary
#             summary, summary_sent_scores = summarize(sent_scores, 3)
#             #print(titles[number-1] + '\n')
#             #print(summary)
#             array2.append(summary)
            
#             #print('\n')
#         except IndexError:
#             pass
#         return array2

#     #USE MULTIPROCESSING HERE
    
#     def main():
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             final_urls = urls[:5]
#             results = [executor.map(finalise, url) for url in urls]
#             return array2

#     if __name__ == '__main__':
#         print('STARTING MULTIPROCESSING')
#         main()
        
#     return ['array2','array2','array2','array2','array2']

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

# summaries = []
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         print("STARTING MULTIPROCESSING")
#         results = executor.map(finalise, urls) 
        
#         for result in results:
#             summaries.append(result)
#             # print(result)

# if summaries != []:
#     final_summary = summaries
#     print(final_summary)

# def run():
#     if __name__ == '__main__':
#         pool = multiprocessing.Pool(processes=3)
#         summaries = pool.map(finalise, urls)
#         print(summaries)
#         while summaries == None:
#             pass
#         return summaries
# hello = run()
# print(hello)

def run():
    if __name__ == '__main__':
        pool = multiprocessing.Pool()
        summaries = [pool.map(finalise, urls)]
        pool.close()
        pool.join()
        return summaries
hello = run()
if hello != None:
    world = hello
    print(world[0][0])