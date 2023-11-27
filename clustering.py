import numpy as np
import pandas as pd
import chart_studio.plotly as plotly

def OPTICS_clustering(minsamples, calc_metric, matrix, idx_to_mid):
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot
    from sklearn.preprocessing import normalize
    init_notebook_mode(connected=True) 
    from sklearn.cluster import OPTICS
    


    clust = OPTICS(min_samples=minsamples, metric=calc_metric)
    normed_matrix=matrix
    clust.fit(normed_matrix)


    reachability = clust.reachability_[clust.ordering_]
    names=np.array(list(idx_to_mid.values()))[clust.ordering_]
    print('Number of outliers is: '+ str(np.sum(clust.labels_ == -1))) #it gives the number of outliers


    scatter  =go.Scatter(x= [i for i in range(len(names))], 
                        y= reachability,
                        text=names
                            )

    # bars = go.Bar(x = center_, y = y_)

    data = [scatter]
    iplot(data)
    return(clust) 

def showclusternb(n, idx_to_mid, clust):
    #n is the nb of cluster which we want to see the result
    #idx_to_mid is map of index to name of attribute
    # #clust is the result model of otics clustering 
    nb=n
    outlieridx_to_mid=idx_to_mid
    outlier1_optcluster=clust
    nameattdf1=pd.DataFrame()
    nameattdf1['name']=outlieridx_to_mid.values()
    nameattdf1['class']=outlier1_optcluster.labels_.tolist()
    nbofClust=nameattdf1['class'].nunique() - 1
    print('Number of clusters is: ' + str(nameattdf1['class'].nunique() - 1))
    if n < nbofClust:
        nameattdf1['reachability']=outlier1_optcluster.reachability_[outlier1_optcluster.labels_]
        print(nameattdf1.name[nameattdf1['class']==nb].tolist())
    else:
        print('enter a number between 0 to ' + str(nbofClust)) 
    return(nbofClust,nameattdf1)

def newclassnum(x, nbofclust, classofoutliers,nbiteration):
    #x is the row of dataframe
    #nbofclust is defining the number of cluster of first iteration to pass to second iteration to change the class number from 0 to 0+nbofcluster and so on.
    #classofoutliers in different iteration is -1.
    #nbiteration : is the number of iteration when clustering is running, then when the clusters want to join from different iteration we can follow the new class number
    newnb=x["class"]
    if newnb!= classofoutliers:
        gennb=newnb+nbofclust
    else:
        gennb=-1*nbiteration
    return gennb