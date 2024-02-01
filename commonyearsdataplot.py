import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from clustereddf_subsets import clustereddf

def common_years2(dfs):  
    #generates a list of years for whih the data is present for both sites
    for i in range(len(df2)):
        year=int(str(df2['TIMESTAMP'].iloc[i])[:4])
        if year in year_list2:
            continue
        else:
            year_list2.append(year)
    return [year for year in year_list1 if year in year_list2]


def common_years(list_of_dfs):
    common_years_list = []

    # Initialize common_years_list with the years from the first DataFrame
    df=list_of_dfs[0]
    first_df_years = set(int(str(df['TIMESTAMP'].iloc[i])[:4])  for i in range(len(df)))
    common_years_list.extend(first_df_years)

    # Iterate through the rest of the DataFrames and update common_years_list
    for df in list_of_dfs[1:]:
        current_years = set(int(str(df['TIMESTAMP'].iloc[i])[:4]) for i in range(len(df)))
        common_years_list = list(set(common_years_list).intersection(current_years))

    return common_years_list


def common_years_df(dataframes=[],commonyears=[]):        #generates the dataframes for common years
    if commonyears==[]:
        startyear=common_years(dataframes)[0]
        endyear=common_years(dataframes)[-1]
        
    else:
        startyear=commonyears[0]
        endyear=commonyears[-1]


    newdataframes=[]
    for df1 in dataframes:
        df1new=df1[(df1['TIMESTAMP']>= (startyear*10**4+101)) & (df1['TIMESTAMP']<= (endyear*10**4 + 1231))].reset_index(drop=True)
        newdataframes.append(df1new)
    #df2new=df2[(df2['TIMESTAMP']>= (startyear*10**4+101)) & (df2['TIMESTAMP']<= (endyear*10**4 + 1231))].reset_index(drop=True)
    return newdataframes

def commonyearsplot(dataframes=[],commonyears=[],titles=[]):

    plotdata=[]
    data_frames=common_years_df(dataframes,commonyears)
    if commonyears==[]:
        cy=common_years(dataframes)
    else:
        cy=commonyears
    #generates the plotting data for each year

    plotdata=[]
    for j in range(len(data_frames)):
        df=data_frames[j]
        plotdata.append([f'{titles[j]}',
                          list(df[df['Clusters'].ne(df['Clusters'].shift())]['Clusters'].items()) 
                        ])

    for i,df in enumerate(data_frames):
        plotdata[i][1].append((len(df),plotdata[i][1][-1][1]))
    print(plotdata)
    #plotting of data for each year

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(9,5))

    #import matplotlib.colormaps as cm
    #colormap = plt.cm.get_cmap('Set2', len(np.unique(dataframes[0]['Clusters'])))



    for y in plotdata:
        color={}
        color_cluster=[]
        for j in y[1]:
            cluster=j[1]
            if cluster not in color_cluster:
                color_cluster.append(cluster)
        color[color_cluster[0]]='darkturquoise'
        if len(color_cluster)==2: color[color_cluster[1]]='purple'
        if len(color_cluster)==3: 
            color[color_cluster[1]]='slategrey'
            color[color_cluster[2]]='green'
        alphalst={color_cluster[0]:0.05, color_cluster[1]:0.3}
        if len(color_cluster)==3: alphalst[color_cluster[2]]=0.6
        for i in range(len(y[1])-1):
            h=y[1][i+1][0]-y[1][i][0]
            b=y[1][i][0]
            #c=colourr(
            
            c=y[1][i][1]
            col=color[c]
            bar= ax.bar(f'{y[0]}',h,    color=col,       bottom=b,alpha=0.1 if col =='blue' else 0.3)                        # 

    #ax.legend(np.unique(dataframes[0]['Clusters']))
    #plt.title('Comparison of Sites')
    ax.set_xlabel('Observation Sites',fontweight='bold')
    #ax.set_ylabel('Year',fontweight='bold')
    #ax.set_ylabel('')
    # Set the x-axis labels to bold
    plt.xticks(titles, fontweight='bold')
    # Add years as labels along the y-axis
    years_pos=np.arange(len(cy))*364+180
    ax.set_yticks(years_pos,labels=cy, fontweight='bold')#+[cy[-1]+1])
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    months_pos=[i*30 for i in range(1,13)]
    ax.set_yticks(months_pos,labels=months,fontweight='bold')
    #ax.set_yticks([])
    #for j in range(len(cy)+1):
        #plt.axhline(j*364,color='black', linestyle='--',linewidth=0.75)
    fig.savefig('ComparisonSites')
    plt.show()