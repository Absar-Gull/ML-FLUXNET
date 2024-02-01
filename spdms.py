import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def getSPDMs(data, wsize):
    
    winsize = wsize
    start = 0
    covmat = []            #list containing elements of each covariance matrix as a list
    covar = []             #the list of covariance matrices
    columns = data.columns
    dim = len(columns) - 1
    cluster_idx = []       
 
    while start+winsize < len(data):
        cluster_idx.append(start)
        data_batch = data[start: start + winsize]    #divides the data into fragments defined by winsize and starting point

        ls_data_batch = []    #for a given data_batch, generates a list that contains each column as a list 

        for i in range(len(columns)):
            ls_data_batch.append(   
                                data_batch[columns[i]].values.tolist()  #for each column of the data_batch, 
                                                                        #this converts values of each column to list item
                                )   

        cov = np.cov(np.array(ls_data_batch))    #generates covariance matrix for each array defined by ls_data_batch 
        covar.append(cov)
        upper = np.triu(cov, k=0)   #generates the upper triangular covariance matrix
        mask = np.triu_indices(dim)
        newupp = list(upper[mask])  #contains the non-zero elements of upper triangular covariance matrix as 
        covmat.append(newupp)

        start= start + winsize   #updates the starting point

    return covmat, covar, cluster_idx
