import regimes 
import numpy as np
import pandas as pd
from  clustereddf_subsets import clustereddf
import matplotlib.pyplot as plt

def groupregimesplot(DF,climateparameters,ecosystemparameters,k,winsize,years=None):
    df_cli=clustereddf(DF,climateparameters,k,winsize)#['Clusters']
    df_eco=clustereddf(DF,ecosystemparameters,k,winsize)
    df_list=[df_cli,df_eco]
    startyear=int(str(DF['TIMESTAMP'].iloc[0])[:4])
    if years==None:
        years=(len(df_cli)/364)+1
    fig,ax=plt.subplots()#figsize=(9,5))
    
    for j,df in enumerate(df_list):

        y=0.33*(j+1)
        ax.plot(df.index,[y]*len(df),linewidth=2.5,label= 'Climate' if j==0 else 'Ecosystem')
        shiftpoints=list(df[df['Clusters'].ne(df['Clusters'].shift())]['Clusters'].items())
        #shiftpoints.append((len(df),df['Clusters'].iloc[-1]))
        sp=shiftpoints
        color={}
        #color[df['Clusters'].value_counts().index[0]]='red'
        #color[df['Clusters'].value_counts().index[1]]='green'
        #if k==3: color[df['Clusters'].value_counts().index[2]]='blue'
        color_cluster=[]
        for dp in sp:
            cluster=dp[1]
            if cluster not in color_cluster:
                color_cluster.append(cluster)
    
        color[color_cluster[0]]='red'
        color[color_cluster[1]]='green'
        if len(color_cluster)==3: 
            color[color_cluster[2]]='blue'
            
        #prev_cluster=None
        for i in range(len(sp)-1):
            start = sp[i][0]   #ta graph he points where each regime begins
            end=sp[i+1][0]   
            cluster=sp[i][1]
            #print(start,end,cluster)
            plt.axvspan(start, end,y-0.16,y+0.16, color=color[cluster], alpha=0.2)
            plt.axvline(start,y-0.16,y+0.16,linestyle='--',color='black')
            plt.text(start,y,s=f'R$_{cluster}$')
            if end>years*364:
                break
           
    plt.ylim(0,1)
    plt.xlim(0,min([years*364,len(df_cli)]))
    for i in range(int(years)):
       plt.axvline(i*364,ymax=0.16,color='black',linestyle='--')
    ax.set_yticklabels([])
    minn=min([years,int(len(df_cli)/364)+1])
    ax.set_xticks([(i)*364+182 for i in range(minn)],labels=[startyear+i for i in range(minn)])
    if minn>12:
        plt.xticks(rotation=-30)
    plt.ylabel('')

    legend_handles=[]
    colr={0:'red',1:'green'}
    if len(df_cli['Clusters'].unique())==3:
        colr[2]='blue'
    for label, colors in sorted(colr.items()):
        legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors, markersize=10,alpha=0.5, label=f'Regime {label+1}'))
    regimescolor=plt.legend(handles=legend_handles,loc=4)
    plt.legend(reverse=True,loc=1)
    plt.gca().add_artist(regimescolor)
    plt.show()

def yearlygroupregimeplot(DF,climateparameters,ecosystemparameters,k,winsize,startingyear,endingyear=None,title=None):
    
    df_cli=clustereddf(DF,climateparameters,k,winsize)#['Clusters']
    df_eco=clustereddf(DF,ecosystemparameters,k,winsize)
    if endingyear==None: endingyear=startingyear
    df_cli=df_cli[(df_cli['TIMESTAMP']>=startingyear*10**4+101) & (df_cli['TIMESTAMP']<=endingyear*10**4+1231)].reset_index(drop=True)
    df_eco=df_eco[(df_eco['TIMESTAMP']>=startingyear*10**4+101) & (df_eco['TIMESTAMP']<=endingyear*10**4+1231)].reset_index(drop=True)
    df_list=[df_cli,df_eco]
    startyear=int(str(DF['TIMESTAMP'].iloc[0])[:4])
    
    #if years==None:
    #    years=(len(df_cli)/364)+1
    years=endingyear-startingyear+1
    fig,ax=plt.subplots()#figsize=(9,5))
    
    for j,df in enumerate(df_list):

        y=0.33*(j+1)
        ax.plot(df.index,[y]*len(df),linewidth=2.5,label= 'Climate' if j==0 else 'Ecosystem')
        shiftpoints=list(df[df['Clusters'].ne(df['Clusters'].shift())]['Clusters'].items())
        shiftpoints.append((len(df),df['Clusters'].iloc[-1]))
        sp=shiftpoints
        color={}
        #color[df['Clusters'].value_counts().index[0]]='red'
        #color[df['Clusters'].value_counts().index[1]]='green'
        #if k==3: color[df['Clusters'].value_counts().index[2]]='blue'
        color_cluster=[]
        for dp in sp:
            cluster=dp[1]
            if cluster not in color_cluster:
                color_cluster.append(cluster)
    
        color[color_cluster[0]]='red'
        color[color_cluster[1]]='green'
        if len(color_cluster)==3: 
            color[color_cluster[2]]='blue'
        if j==0:
            color[color_cluster[1]]='blue'
            color[color_cluster[2]]='green'
        #prev_cluster=None
        for i in range(len(sp)-1):
            start = sp[i][0]   #ta graph he points where each regime begins
            end=sp[i+1][0]   
            cluster=sp[i][1]
            #print(start,end,cluster)
            plt.axvspan(start, end,y-0.16,y+0.16, color=color[cluster], alpha=0.3)
            plt.axvline(start,y-0.16,y+0.16,linestyle='--',color='black')
            #plt.text(start,y,s=f'R$_{cluster}$')
            #if end>years*364:
            #    break
           
    plt.ylim(0,1)
    plt.xlim(0,min([years*364,len(df_cli)]))       
       
    for y in range(years*12):
        m=364*y
        plt.axvline(m,ymax=0.165,color='black')
        #for i in range(1,12):
        #    plt.axvline(i*30+m,ymax=0.1,color='black',linestyle='--')
    ax.set_yticklabels([])
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if years==1:
        ax.set_xticks([i*30 for i in range(years*12)],labels=months)
        plt.xlabel(f'Year: {startingyear}')
    yearlist=[]
    for i in range(startingyear,endingyear+1):
        yearlist.append('Jan '+str(i))
        yearlist.append('Apr '+str(i))
        yearlist.append('Jul '+str(i))
        yearlist.append('Oct '+str(i))
    if years>=2: 
            ax.set_xticks([90*(i)+(364*y)+14 for y in range(years) for i in range(4) ],labels=yearlist)
            plt.xticks(rotation=90)
    plt.ylabel('')
    


    #plt.xlabel(f'{yearlist}')
    #yearslabel=plt.legend(handles=legend_handles,loc=4)
    plt.legend(reverse=True,loc=1)
    #plt.gca().add_artist(yearslabel)
    plt.title(f'{title}')#\nYear:{yearlist}')
    fig.tight_layout()
    fig.savefig('Hainich_Regimes')
    plt.show()