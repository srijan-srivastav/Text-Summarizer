import bs4 as bs
import urllib.request
import re
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import heapq
from nltk.stem import WordNetLemmatizer

def webScraper(url):
    
    scraped_data = urllib.request.urlopen(url)

    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article, 'lxml')

    paragraphs = parsed_article.find_all('p')

    text_article = ""

    for para in paragraphs:
        text_article += para.text

    return text_article


def removeReferences(text):
    cleaned_text = re.sub(r'\[[0-9]*\]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text


def removeSpecialChars(text):
    cleaned_text = re.sub('[^a-zA-Z]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text


def createFreqDictionary(formatted_text_article):
    stop_words = stopwords.words('english')
    
    lemmatizer_obj = WordNetLemmatizer()

    frequency_of_words = {}
    for word in word_tokenize(formatted_text_article):
        if word not in stop_words:
            root_word = lemmatizer_obj.lemmatize(word)
            if root_word not in frequency_of_words.keys():
                frequency_of_words[root_word] = 1
            else:
                frequency_of_words[root_word] += 1

    return frequency_of_words

def findWeightedFrequency(frequency_of_words):
    max_freq = max(frequency_of_words.values())
    
    for word in frequency_of_words.keys():
        frequency_of_words[word] = (frequency_of_words[word]/max_freq)


def calculateSentenceScores(sentence_list, frequency_of_words, max_sent_len):

    lemmatizer_obj = WordNetLemmatizer()

    sent_scores = {}
    for sent in sentence_list:
        for word in word_tokenize(sent):
            root_word = lemmatizer_obj.lemmatize(word)
            if root_word in frequency_of_words.keys():
                if(len(sent.split(" "))) < max_sent_len:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = frequency_of_words[root_word]
                    else:
                        sent_scores[sent] += frequency_of_words[root_word]

    return sent_scores

def returnSummary(sent_scores, top_n_sents):
    
    summary_sentences = heapq.nlargest(top_n_sents, sent_scores, key=sent_scores.get)

    summary = ' '.join(summary_sentences)  
    return summary

def textSummarization(url, max_sent_len = 30, top_n_sents = 5):
    
    text_article = webScraper(url)
                              
    text_article = removeReferences(text_article)
                              
    formatted_text_article = removeSpecialChars(text_article)
    
    sentence_list = sent_tokenize(text_article)
    
    frequency_of_words = createFreqDictionary(formatted_text_article)
    
    findWeightedFrequency(frequency_of_words)
    
    sent_scores = calculateSentenceScores(sentence_list, frequency_of_words, max_sent_len)
    
    summary = returnSummary(sent_scores, top_n_sents)

    return summary

