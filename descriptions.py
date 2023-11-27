import io
import pickle
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import collections


def replacementdictinary():
    with open('PROCLAIM/replacementdictinary.txt', 'rb') as handle:
        replacementdictinary = pickle.load(handle)
    return replacementdictinary

#adding new word a which should replace with word b in the descriptions to the existing dictionary
def add_replacementdictinary(replacementdictinary,a,b):
     replacementdictinary[a]=b
     return replacementdictinary

def domainstopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.remove('y')
    #stop_words.remove('s')
    stopwords=['since','along','caused','ed','etc','eg','value','per','within','unit','number','well','sample','record','h','user','bore','hole','line','\'S ','two','internet']
    for item in stopwords:
        stop_words.append(item)
    return stop_words

def add_domainstopwords(listofwords):
    stopwords=domainstopwords()
    for item in listofwords:
        stopwords.append(item)
    return stopwords

def word_count(strg):
    counts = dict()
    if isinstance(strg,str):
        words = strg.split()

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts

def bigram2abbrdictinary():
    with open('PROCLAIM/bigramtoabbr.txt', 'rb') as handle:
        bigram2abbr = pickle.load(handle)
    return bigram2abbr

def add_bigram2abbrdictinary(bigram2abbrdictinary,a,b):
    bigram2abbrdictinary[a]=b
    return bigram2abbrdictinary

wpt = nltk.WordPunctTokenizer()
stop_words= domainstopwords()
replacementdic=replacementdictinary()
bigram2abbr=bigram2abbrdictinary()
def normalize_document(row, stop_words):
    # lower case and remove special characters\whitespaces
    doc=row.descr
    doc=doc.replace('_',' ')
    doc=doc.replace('-',' ')
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    if doc.startswith('FROM'):
        doc=None
    if doc!= None:
        doc = doc.lower()
        doc = doc.strip()
        for item in bigram2abbr:
            doc=doc.replace(item,bigram2abbr[item])
        # tokenize document
        tokens = wpt.tokenize(doc)
        reptokens=[replacementdic[token] for token in tokens if token in replacementdic]
        remtokens=[token for token in tokens if token not in replacementdic]
        tokens=reptokens+remtokens
        # filter stopwords out of document
        filtered_tokens = [token for token in tokens if token not in stop_words]
        ps = PorterStemmer()
        stemmed_words=[]
        for w in filtered_tokens:
            stemmed_words.append(ps.stem(w))
        # re-create document from filtered tokens
        doc = ' '.join(stemmed_words)
        #print(doc)
        return doc

def normalize_document_label(row,stop_words):
    # lower case and remove special characters\whitespaces
    doc=row.descr
    doc=doc.replace('_',' ')
    doc=doc.replace('-',' ')
    doc=doc.replace('\'',' ')
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    #stop_words = nltk.corpus.stopwords.words('english')
    if doc.startswith('FROM'):
        doc=None
    if doc!= None:
        doc = doc.lower()
        doc = doc.strip()
        for item in bigram2abbr:
            doc=doc.replace(item,bigram2abbr[item])
        # tokenize document
        tokens = wpt.tokenize(doc)
        reptokens=[replacementdic[token] for token in tokens if token in replacementdic]
        remtokens=[token for token in tokens if token not in replacementdic]
        tokens=reptokens+remtokens
        # filter stopwords out of document
        filtered_tokens = [token for token in tokens if token not in stop_words]
        # re-create document from filtered tokens
        doc = ' '.join(filtered_tokens)
        #print(doc)
        return doc


def get_dictionary_list(df2,attribute,columnname,filteredproperties) :
    # mnemonic is the column name for attributes
    dictionarylist = []
    BOW=columnname
    mnemonic=attribute
    for i,item in enumerate(filteredproperties):
        #print(i,item)
        counts={}
        sorted_count={}
        idx=df2[df2[mnemonic]==item].index.tolist()
        words=df2[BOW][df2.index.isin(idx)].tolist()
        #print(words)
        for word in words:
            if isinstance(word, str):
                #print(word)
                #print(len(word.split()))
                if len(word.split())==1:
                    if word in counts:
                            counts[word] += 1
                    else:
                            counts[word] = 1
                else:
                        stri=word.split()
                        for item1 in stri:
                            #print(item1)
                            if item1 in counts:
                                counts[item1] += 1
                            else:
                                counts[item1] = 1
        #print(counts)
        sorted_dict = sorted(counts, key=counts.get, reverse=True)
        #print(sorted_dict)
        for r in sorted_dict:
            sorted_count[r]=counts[r]
        #sorted_dict = collections.OrderedDict(counts)
        #sorted_dict=sorted(counts.items(), key=lambda x: x[1], reverse=True)
        #count1={list(counts.keys())[list(counts.values()).index(k)]: k for k in sorted(counts.values())}
        #sorted_dict={k: k for k in sorted(counts.values())}
        if len(sorted_count)>=5:
            sorted_count={list(sorted_count.keys())[k]:list(sorted_count.values())[k] for k in range(5)}
        else:
            sorted_count={list(sorted_count.keys())[k]:list(sorted_count.values())[k] for k in range(len(sorted_count))}
        #print(sorted_count)
        dictionarylist.append(sorted_count)
        #print(dictionarylist)
    return dictionarylist
