import regimes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Normalization (Standard)
def normalize(data, type='minmax'):

    if type=='std':
        return (np.array(data) - np.mean(data))/np.std(data)
        
    elif type=='minmax':
        return (np.array(data) - np.min(data))/(np.max(data) - np.min(data))

def yearlyplot(data1,k,winsize,title,parameters=None,startyear=None,endyear=None):

    TS=data1["TIMESTAMP"]
    if parameters==None:
        data = data1[["TA_F","NEE_VUT_REF","GPP_DT_VUT_REF","RECO_NT_VUT_REF","LE_F_MDS","VPD_F"]]
    else:
        data=data1[parameters]
    
    #normalization of data
    data=data.apply(normalize)
    
    #generating regimes and clusters
 
    clusters, cluster_idx = regimes.get_regimes(data, winsize, k, 'Riemannian')

    #creating new dataframe including the cluster for each data point and timestamp
    clusters_extended = []

    for i in range(len(clusters)):

        val = clusters[i]
        for j in range(winsize):
            clusters_extended.append(val)
        
    datanew = data.iloc[:len(clusters_extended), :].copy()
    datanew['Clusters'] = clusters_extended
    datanew.insert(loc=0,column="TIMESTAMP",value=TS)

    #generates the data for each year from 2000 to 2012

    def yearly_DA(data,year):
        datayear=(data['TIMESTAMP']>= (year*10**4+101)) & (data['TIMESTAMP']<= (year*10**4 + 1231))
        return data[datayear].reset_index(drop=True)
        
    if startyear==None: startyear=int(str(datanew['TIMESTAMP'].iloc[0])[:4])
    if endyear==None: endyear=int(str(datanew['TIMESTAMP'].iloc[-1])[:4])
    data_frames=[yearly_DA(datanew,i) for i in range(startyear,endyear)]

    #generates the plotting data for each year

    plotdata=[]
    for j in range(len(data_frames)):
        plotdata.append([j+startyear,
                      list(data_frames[j][data_frames[j]['Clusters'].ne(data_frames[j]['Clusters'].shift())]['Clusters'].items()) 
                    ])
    for y in plotdata:
        y[1].append((365,y[1][-1][1]))
        continue

    #plotting of data for each year

    # Set up the figure and axis
    fig, ax = plt.subplots()

    #import matplotlib.colormaps as cm
    #colormap = plt.cm.get_cmap('Set2', len(np.unique(clusters)))
    #color = {0: 'red', 1: 'green'}
    #if len(np.unique(clusters))==3:
    #    color[2]= 'grey'
    #if len(np.unique(clusters))==4:
    #    color[3]= 'yellow'
    #colors={}
    for y in plotdata:
        color={}
        color_cluster=[]
        for dp in y[1]:
            cluster=dp[1]
            if cluster not in color_cluster:
                color_cluster.append(cluster)
    
        color[color_cluster[0]]='red'
        color[color_cluster[1]]='green'
        if len(color_cluster)==3: color[color_cluster[2]]='blue'
        if len(color_cluster)==4: color[color_cluster[3]]= 'yellow'
        for i in range(len(y[1])-1):
            h=y[1][i+1][0]-y[1][i][0]
            b=y[1][i][0]
            #c=colourr(
            c=y[1][i][1]
            bar= ax.bar(f'{y[0]}',h,color=color[c],bottom=b,alpha=0.6)
            #colors[c]=f'{color[c]}'
    ax.set_xlabel('Year')
    if endyear-startyear>12:
        plt.xticks(rotation=30)
    ax.set_ylabel('Days of Year')
    plt.title(title)

    #legend_handles=[]
    #for label, colors in sorted(color.items()):
   #     legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors, markersize=10,alpha=0.5, label=f'Regime {label}'))

    # Show the custom legend
    #plt.legend(handles=legend_handles)
    fig.savefig(title)
    
    plt.show()