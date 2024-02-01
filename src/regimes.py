#import parameters
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from spdms import getSPDMs
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statsmodels.tsa.stattools import adfuller
plt.rcParams['figure.dpi'] = 200


from sklearn.cluster import KMeans
from pyriemann.clustering import Kmeans
from sklearn import metrics
from scipy.spatial.distance import cdist

def pyriemann_clusters(data, k):
    
    #Clustering by k-means with SPD matrices as inputs.
    #https://pyriemann.readthedocs.io/en/latest/generated/pyriemann.clustering.Kmeans.html#pyriemann.clustering.Kmeans

    kmeans = Kmeans(k, metric='riemann', tol=1e-3, init='random')
    kmeans.fit(data)
    labels = kmeans.predict(data)
        
    return labels


def get_regimes(data, wsize, k, dist_metric):
    
    covmat, covar, cluster_idx = getSPDMs(data, wsize)
    
    if dist_metric == 'Euclidean':
        
        kmeans = KMeans(n_clusters=k, random_state=0, n_init=1).fit(covmat)
        clusters = list(kmeans.labels_)
        print(f"Clusters: {list(kmeans.labels_)}")
    
    else:
        clusters = pyriemann_clusters(np.array(covar), k)     

    return clusters, cluster_idx

def get_reduced_set(df):
    
    corr = data.corr()
    cls = corr.iloc[0][:].values.tolist()
    selected_idx = np.where(cls>0.50)[0].tolist()

    reduced_df = df.iloc[:, selected_idx].copy()
    return reduced_df


def plot_regimes(data, clusters, cluster_idx, winsize, dtype='real'):
     
    if dtype == 'real':
          
        # Plot regimes in real data

        toplot = [f"{i}" for i in data]    #   

        data.plot(use_index=True, cmap='tab10', figsize=(8, 4), linewidth=0.75)
        prev_cluster=None
        for c in range(len(cluster_idx)):

            val = cluster_idx[c]   #the points where each cluster begins
            cluster=clusters[c]    

            #Color coding of clusters
            #Each cluster has a unique color and are separated by a black-dash line
            if cluster == 0: 
                plt.axvspan(val, val+winsize, color='blue', alpha=0.1)
            if cluster == 1:
                plt.axvspan(val, val+winsize, color='red', alpha=0.1)    
            if cluster == 2:
                plt.axvspan(val, val+winsize, color='yellow', alpha=0.1)        
            if cluster == 3:
                plt.axvspan(val, val+winsize, color='green', alpha=0.1)    
            if prev_cluster!=cluster:
                plt.axvline(x=val, color='black', linestyle='--', linewidth=0.75)
            prev_cluster=cluster
        plt.ylim(0, 1.6)
        plt.xlabel('')
        plt.ylabel('normalized values')
        plt.show()

    else:
        # Plot regimes in synthetic data

        toplot = ['Z1', 'Z3', 'Z5']
        colors = ['r', 'g', 'b', 'y', 'c']

        t = np.arange(0, cluster_idx[-1]+winsize)
        start = 0

        # for c in range(len(clusters)):
            
        #     if clusters[c] == 0:
        #             marker = '-'
        #     elif clusters[c] == 1:
        #             marker = '-'
        #     elif clusters[c] == 2:
        #             marker = '-'
        #     for i in toplot:
                
        #         data[i].plot(use_index=True)
        #         plt.legend(toplot)
        # #         plt.plot(t[start: start+winsize], data[toplot[i]].values[start: start + winsize], colors[i]+marker)
        # #         plt.plot(t[start: start + winsize], data[toplot[i+1]].values[start: start + winsize], color)
        # #         plt.plot(t[start: start + winsize], data[toplot[i+2]].values[start: start + winsize], color)
                
        #     start = start + winsize

        plt.figure(figsize=(6, 3))
        col = ['teal', 'slategrey', 'goldenrod']
        mark = ['-', '--', '.-.']
        for i, v in enumerate(toplot):
            # data.plot(use_index=True, figsize=(10, 3), linewidth=0.75, alpha=0.66, color=['green', 'blue', 'red'])
            plt.plot(data[v], mark[i], color=col[i])
        #   plt.plot(t[start: start+winsize], data[toplot[i]].values[start: start + winsize], colors[i]+marker)
        #   plt.plot(t[start: start + winsize], data[toplot[i+1]].values[start: start + winsize], color)
        #   plt.plot(t[start: start + winsize], data[toplot[i+2]].values[start: start + winsize], color)


        plt.legend(toplot)
        for c in range(len(cluster_idx)):
                
            val = cluster_idx[c]
            print(f'{val} to {val+winsize}')
            if clusters[c] == 0:
                plt.axvspan(val, val+winsize, label='0',facecolor='green', alpha=0.15)    
            if clusters[c] == 1:
                plt.axvspan(val, val+winsize, facecolor='white', alpha=0.25)  
            if clusters[c] == 2:
                plt.axvspan(val, val+winsize, facecolor='red', alpha=0.15)  
            if clusters[c] == 3:
                plt.axvspan(val, val+winsize, facecolor='yellow', alpha=0.15)  
        
        plt.axvline(x=364, color='red')
        # plt.text(305, 1.10, 'Change Point', fontsize=9.0, fontweight='bold')
        plt.axvline(x=720, color='red')
        # plt.text(670, 1.10, 'Change Point', fontsize=9.0, fontweight='bold')
        plt.ylim(0, 1.3)
        plt.legend(['$Z_{1}$', '$Z_{2}$', '$Z_{3}$'], loc='upper left', fontsize=50, prop=dict(weight='bold'))
        # plt.title("Euclidean", fontsize=15)
        plt.ylabel("window=90", fontsize=15)
        # plt.xlabel('data points', fontsize=10)
        # plt.savefig("../res/synwin90EE.pdf")

        plt.show()
