import numpy as np
import os

from utils import convert, distance, iou
import cluster_slider
import cluster_surveys


def load_all_surveys(xml_master_dir):
    dfs = []
    for r,dirs,paths in os.walk(xml_master_dir):
        dfs.append([convert.xml2df(os.path.join(r,s_i)) for s_i in paths if s_i.endswith('.xml')])
    return dfs


def CSFD_plot(dfs,df_filter=None):
    resolution=6
    diams = []
    for i,tile in enumerate(dfs):
        for j,survey in enumerate(tile):
            if df_filter is not None:
                survey = df_filter(survey)
            annots_on_tile,_ = convert.df2np(survey)
            diams += list(annots_on_tile[:,4]*resolution)
    print(np.min(diams),np.max(diams))
    bin_edges = np.power(10,np.linspace(np.log10(18),np.log10(1939),28))
    dys,_ = np.histogram(diams,bin_edges)
    ys = np.cumsum(dys[::-1])[::-1]/(12*12**2) #divided by area in km^2
    smooth_ys = np.array([np.mean(ys[max(0,i-1):min(len(ys),i+2)]) for i in range(len(ys))])

    #check for zero-values at the end and remove (messes up log plot)
    while True:
        if ys[-1]==0:
            bin_edges = bin_edges[:-1]
            ys = ys[:-1]
            smooth_ys = smooth_ys[:-1]
        else:
            return bin_edges, ys, smooth_ys

def number_filter(n):
    def func(df):
        if isinstance(n,list):
            return df.loc[(df['conf'] >= n[0]) & (df['conf'] < n[1])]
        else:
            return df.loc[df['conf'] == n]
    return func


if __name__=='__main__':
    import sys
    import matplotlib.pyplot as plt

    annotation_dir = os.path.join(os.path.dirname(__file__),'../data/annotations')
    raw_dfs = load_all_surveys(os.path.join(annotation_dir,'raw'))
    clustered_dfs = load_all_surveys(os.path.join(annotation_dir,'clustered'))



    c_bins,c_ys,c_smooth_ys = CSFD_plot(clustered_dfs)
    r_bins,r_ys,r_smooth_ys = CSFD_plot(raw_dfs)

    n1_bins,n1_ys,n1_smooth_ys = CSFD_plot(clustered_dfs,df_filter=number_filter(1))
    n234_bins,n234_ys,n234_smooth_ys = CSFD_plot(clustered_dfs,df_filter=number_filter([2,5]))
    n56_bins,n56_ys,n56_smooth_ys = CSFD_plot(clustered_dfs,df_filter=number_filter([5,7]))

    fig,ax = plt.subplots(figsize=(7,6))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(c_bins[:-1]+np.diff(c_bins)/2,c_ys,alpha=0.8,marker='o',c='r',fillstyle='none',label='clustered annotations')
    ax.plot(r_bins[:-1]+np.diff(r_bins)/2,r_ys,alpha=0.7,marker='s',c='b',fillstyle='none',label='unclustered annotations')
    ax.plot(n1_bins[:-1]+np.diff(n1_bins)/2,n1_smooth_ys,alpha=0.8,c='k',marker='v',linewidth=0.8,linestyle='--',fillstyle='none',label='clusters with only 1 annotation')
    ax.plot(n234_bins[:-1]+np.diff(n234_bins)/2,n234_smooth_ys,alpha=0.8,c='k',marker='*',linewidth=0.8,linestyle='--',fillstyle='none',label='clusters with 2-4 annotations')
    ax.plot(n56_bins[:-1]+np.diff(n56_bins)/2,n56_smooth_ys,alpha=0.8,c='k',marker='P',linewidth=0.8,linestyle='--',fillstyle='none',label='clusters with 5-6 annotations')

    ax.set_xlabel('Diameter ($m$)')
    ax.set_ylabel('Cumulative Size-Frequency ($km^{-2}$)')
    ax.set_xlim(18,2*10**3)
    ax.set_ylim(10**-4,10**1.2)
    ax.grid(True,which='major',linestyle='-',alpha=0.9)
    ax.grid(True,which='minor',linestyle='--',alpha=0.6)
    ax.set_title('Cumulative Crater Size-Frequency Distribution of \nclustered and unclustered annotations\n')
    ax.legend(loc='lower left')
    plt.show()
