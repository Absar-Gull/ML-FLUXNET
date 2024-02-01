import regimes
import numpy as np
import pandas as pd
np.random.seed(1)
# Normalization (Standard)
def normalize(data, type='minmax'):

    if type=='std':
        return (np.array(data) - np.mean(data))/np.std(data)
        
    elif type=='minmax':
        return (np.array(data) - np.min(data))/(np.max(data) - np.min(data))


def clustereddf(df1,parameters,k,winsize):
    df1=df1.dropna()
    TS=df1["TIMESTAMP"]
    df=df1[parameters]
    
    #normalization of data
    df=df.dropna()
    df=df.apply(normalize)
    
    #generating regimes and clusters
 
    clusters, cluster_idx = regimes.get_regimes(df, winsize, k, 'Riemannian')

    #creating new dataframe including the cluster for each data point and timestamp
    clusters_extended = []

    for i in range(len(clusters)):

        val = clusters[i]
        for j in range(winsize):
            clusters_extended.append(val)
        
    datanew = df.iloc[:len(clusters_extended), :].copy()
    datanew['Clusters'] = clusters_extended
    datanew.insert(loc=0,column="TIMESTAMP",value=TS)

    return datanew
