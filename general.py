import pandas as pd
import string
import numpy as np
import math


#this function return filtered properties list based on the chosen Types
def filter_by_type(*args,filepath):
    Typedf= pd.read_csv(filepath, sep=',')
    mylist=[]
    for elem in args:
        if elem!= 'datetime64[ns]':
            elem=string.capwords(elem)
            mylist.append(elem)
        else:
            mylist.append(elem)
    pattern = '|'.join(mylist)
    filteredproperties=Typedf.attribute[Typedf.value.str.contains(pattern)].unique().tolist()
    if any(element is np.NAN for element in mylist):
        filteredproperties.remove(np.nan)
    if len(filteredproperties)==0 and len(mylist)==1:
        filteredproperties=Typedf.attribute[Typedf.value==elem].unique().tolist()
    if len(filteredproperties)==0:
        print('There is not this type of attributes in the dataset')
    return filteredproperties

def map_id_to_name(filteredproperties):
    mid_to_idx = {}
    idx_to_mid = {}
    for (idx, mid) in enumerate(filteredproperties):
        mid_to_idx[mid] = idx
        idx_to_mid[idx] = mid
    return mid_to_idx , idx_to_mid

def find_duplication_dict(possiblemid):
    Duplicates = [(key_a,key_b) for  key_a in possiblemid for  key_b in possiblemid if (key_a==possiblemid[key_b]) and key_a != key_b]
    return Duplicates