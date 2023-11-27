import os
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import re
import string
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import pickle
from ml_akbc.akbc.descriptions import replacementdictinary
import collections
import numpy as np



def create_newcorpus():
    corpusdir = 'ml_akbc/akbc/' # Directory of corpus.

    newcorpus = PlaintextCorpusReader(corpusdir, '.*')
    return(newcorpus)


#bigram model
def create_bigrammodel(namefile,newcorpus):
    #namefile: name of the csv file we want to change to the corpus
    #newcorpus: created corpus from function create_newcorpus()
    model1 = defaultdict(lambda: defaultdict(lambda: 0))
    nameofcorpus=namefile
    for sentence in newcorpus.sents(nameofcorpus):
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            if w1 is not None and w2 is not None:
                w1=w1.lower()
                w2=w2.lower()
                model1[w1][w2] += 1
    # with open('C:/Users/marman2/ml-lab-akbc/akbc/bigram_model.txt', 'wb') as handle: # I couldn't handle to save the model
    #     pickle.dump(model1, handle)
    return model1

def load_bigrammodel():
    with open('ml_akbc/akbc/bigram_model.txt', 'rb') as handle:
        bigram_model = pickle.load(handle)
    return bigram_model   
    
def create_trigrammodel(namefile,newcorpus):
    #trigram model
    model = defaultdict(lambda: defaultdict(lambda: 0))
    for sentence in newcorpus.sents('oil_corpus.csv'):
        for w1, w2, w3 in trigrams(sentence, pad_right=True, pad_left=True):
            if w1 and w2 and w3 is not None:
                w1=w1.lower()
                w2=w2.lower()
                w3=w3.lower()
                model[(w1, w2)][w3] += 1
    # with open('C:/Users/marman2/ml-lab-akbc/akbc/trigram_model.txt', 'wb') as handle:
    #         pickle.dump(model, handle)
    return model

def load_trigrammodel():
    with open('ml_akbc/akbc/trigram_model.txt', 'rb') as handle:
        trigram_model = pickle.load(handle)
    return trigram_model

def dict_clusterlabeling(df,dictionarylistLABEL,mid_to_idx, trigram_model,bigram_model): 
    #df should have the name 'class','name'
    labels={}
    resultlev1=df
    model1= bigram_model
    model=trigram_model
    replacementdic=replacementdictinary()
    nbclusters = resultlev1['class'].nunique()-1
    print(nbclusters)
    feat_dlistnbclust = [{} for _ in range(nbclusters)]
    final_sorted_feat=[{} for _ in range(nbclusters)]
    for clusternb in range(nbclusters):
        idx_1=resultlev1.name[resultlev1['class']==clusternb].tolist()
        nb=[]
        for i in idx_1:
            terms=dictionarylistLABEL[mid_to_idx[i]]
            terms1=terms
            for word in terms:
                if word in replacementdic:
                    terms1[replacementdic[word]] = terms1.pop(word)
            terms=terms1
            nb.append(terms)
        frequency = {}
        for my_dict in nb:
                for value in my_dict.keys() :
                    if value in frequency :
                        frequency[value] = frequency[value] + my_dict[value]
                    else :
                        frequency[value] = my_dict[value]
        orderedpw={}
        orderedp3g={}
        sorted_dict = sorted( frequency, key= frequency.get, reverse=True)
        sorted_orderedpw={item: frequency[item] for item in sorted_dict[0:6] }
        sorted_orderedpw_head={item: frequency[item] for item in sorted_dict[0:4] }

        for word1 in sorted_orderedpw:
            for word2 in sorted_orderedpw:
                if word1!=word2:
                    label=word1 +' '+word2
                    orderedpw[label]=model1[word1][word2] #bigram model
                    for word3 in sorted_orderedpw:
                        if word3!=word1 and word3!=word2:
                            label=word1 +' '+word2+' '+word3
                            orderedp3g[label]=model[(word1,word2)][word3] #trigram model
        implist={}
        for biterm in orderedpw:
            if orderedpw[biterm]>0:
                fword=biterm.split(' ')[0]
                secword=biterm.split(' ')[1]
                if fword in sorted_orderedpw_head and secword in sorted_orderedpw_head:
                    implist[biterm]= orderedpw[biterm]
        sorted_implist=sorted( implist, key= implist.get, reverse=True)
        sorted_dict1 = sorted(orderedpw, key=orderedpw.get, reverse=True)
        final_sorted_orderedpw={item: orderedpw[item] for item in sorted_dict1[0:5] }
        sorted_dict_3gram = sorted(orderedp3g, key=orderedp3g.get, reverse=True)
        final_sorted_3gram={item: orderedp3g[item] for item in sorted_dict_3gram[0:5] }
        for i in final_sorted_3gram:
            if final_sorted_3gram[i]> 0:
                feat_key = '{}'.format(i)
                if final_sorted_3gram[i]!=1:
                    feat_dlistnbclust[clusternb][feat_key]=final_sorted_3gram[i]*20
                else:
                    feat_dlistnbclust[clusternb][feat_key]=final_sorted_3gram[i]
        if sorted_implist==[]:
            for i in final_sorted_orderedpw:
                feat_key = '{}'.format(next(iter(sorted_orderedpw.keys())))
                feat_dlistnbclust[clusternb][feat_key]=1
        else:
            feat_key = '{}'.format(sorted_implist[0])
            feat_dlistnbclust[clusternb][feat_key]=implist[sorted_implist[0]]
        if sorted_orderedpw!={}:
            feat_key = '{}'.format(next(iter(sorted_orderedpw.keys())))
            feat_dlistnbclust[clusternb][feat_key]=1
        sorted_feat = sorted(feat_dlistnbclust[clusternb], key=feat_dlistnbclust[clusternb].get, reverse=True)
        final_sorted_feat[clusternb]={item: feat_dlistnbclust[clusternb][item] for item in sorted_feat}
        if feat_dlistnbclust[clusternb]!={}:
            labels[clusternb]=next(iter(final_sorted_feat[clusternb].keys()))
        else:
            labels[clusternb]=''
    print(labels)
    return(final_sorted_feat,labels)

def labelizingclusters(row,labels):
    k=False
    for clustnb in labels:
        if row['class']==clustnb:
            k=True
            return(labels[clustnb])
    if k==False:
        return('')

def predictsimlabel(similaritiesp,attribute,idx_to_midp,mid_to_idxp):
    top_values=[]
    top_n_attribute=[]
    simdense=similaritiesp.todense()
    idx=mid_to_idxp[attribute]
    p=simdense[idx]
    A=np.array(p).ravel()
    top_n_idx = np.argsort(A)[-200:]
    top_n_values = [A[i] for i in top_n_idx]
    for i, item in enumerate(top_n_values):
        if item > 0:
            top_n_attribute.append(idx_to_midp[top_n_idx[i]])
            top_values.append(item)
    print(top_n_attribute)
    return(top_n_attribute)
     