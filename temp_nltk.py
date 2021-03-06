import bs4 as bs
import urllib.request
import re
import nltk
import heapq
import validators

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none'}

def url_rize(raw_urls,types):
    if types == 'ss':
        thres   = 26
        sen_num = 5
        key_sen = 3
    elif types == 'ls':
        thres   = 35
        sen_num = 10
        key_sen = 5
    else:
        thres   = 40
        sen_num = 20
        key_sen = 7
    valid = validators.url(raw_urls)
    if valid == True:
        url = raw_urls
        request=urllib.request.Request(url,None,headers)
        source = urllib.request.urlopen(request).read()
        soup = bs.BeautifulSoup(source,'lxml')
        text = ""
        title = soup.find('title').text
        for paragraph in soup.find_all(['p']):
            text += paragraph.text
    else:
        text = raw_urls
       
    text = re.sub(r'\[[0-9]+\]',' ',text)
    text = re.sub(r'\s+',' ',text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W',' ',clean_text)
    clean_text = re.sub(r'\d',' ',clean_text)
    clean_text = re.sub(r'\s+',' ',clean_text)

    sentences = nltk.sent_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')

    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word]=1
            else:
                word2count[word] += 1

    for key in word2count.keys():
        word2count[key] = word2count[key]/max(word2count.values()) 
        
    sent2score = {} 

    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()): 
            if word in word2count.keys():
                if len(sentence.split(' ')) < thres:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        word2count[word] += word2count[word]                 
    best = heapq.nlargest(sen_num,sent2score,key=sent2score.get)
    sents2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()): 
            if word in word2count.keys():
                if len(sentence.split(' ')) < 27:
                    if sentence not in sents2score.keys():
                        sents2score[sentence] = word2count[word]
                    else:
                        word2count[word] += word2count[word] 
    key_points = heapq.nlargest(key_sen,sents2score,key=sents2score.get)
    x = " ".join(best)
    if valid == True:
        return [x,title,key_points]
    else:
        return[x,'Summary',key_points]

