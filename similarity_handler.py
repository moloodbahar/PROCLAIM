from sklearn.feature_extraction import DictVectorizer
import sklearn.preprocessing as pp
import numpy as np


def sparsesimilarity(dic_list):
    dv = DictVectorizer()
    diclist=dic_list
    vector_features = dv.fit_transform(diclist)
    col_normed_mat = pp.normalize(vector_features, axis=1)
    similarities = col_normed_mat * col_normed_mat.T
    return similarities

def distancematrix(similaritymatrix):
    distance = 1-similaritymatrix.toarray()
    distance = np.where(distance<0, 0, distance)
    return distance


def normalizematrix(matrixA,**norm):
    from sklearn.preprocessing import normalize
    normed_matrix = normalize(matrixA, axis=1, norm='l1')
    return normed_matrix

def predictsimatt(similarities,attribute,mid_to_idx,idx_to_mid, n):
        #similarities is sparse matrix of similarity
        #attribute : name of the term which we try to find the most similar one for that
        #mid_to_idx should define the map of terms name as index of similarity matrix
        #idx_to_mid should define the map of name of the columns of similarity matrix
        top_values=[]
        top_n_attribute=[]
        simdense=similarities.todense()
        if attribute in mid_to_idx:
                idx=mid_to_idx[attribute]
                p=simdense[idx]
                A=np.array(p).ravel()
                top_n_idx = np.argsort(A)[-200:]
                top_n_values = [A[i] for i in top_n_idx]
                for i, item in enumerate(top_n_values):
                        if item >= n:
                                top_n_attribute.append(idx_to_mid[top_n_idx[i]])
                                top_values.append(item)
                print(top_values)
                return(top_n_attribute)
        else:
                print('Please Enter a valid attribute name')


def partitioning_matrix(matrix,indexlist):
        normed_matrix=matrix
        idxlist=indexlist
        d=normed_matrix[idxlist]
        m=d.T
        n=m[idxlist]
        g=n.T
        distance3= g
        return(distance3)