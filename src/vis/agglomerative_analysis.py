import numpy as np
import os

from data import convert
import cluster_slider
import cluster_surveys
import distance
import iou


def load_all_surveys(xml_master_dir):
    assert os.path.isdir(xml_master_dir), 'xml_dir is not a directory!'
    dfs = []
    for path in os.listdir(xml_master_dir):
        tile_dir = os.path.join(xml_master_dir,path)
        if os.path.isdir(tile_dir):
            dfs.append([convert.xml2df(os.path.join(tile_dir,s_i)) for s_i in os.listdir(tile_dir)])
    return dfs

def calc_all_nodetrees(dfs,distance_metric):
    nodes = []
    for df in dfs:
        nodes.append(cluster_surveys.agglomerative(df, distance_metric))
    return nodes

def individual_annotation_size_plot(dfs):
    diams = []
    for i,tile in enumerate(dfs):
        for j,survey in enumerate(tile):
            annots_on_tile,_ = convert.df2np(survey)
            diams += list(annots_on_tile[:,4])

    fig,ax = plt.subplots()
    ys,bins,patches = ax.hist(diams,[i for i in range(180)],rwidth=0.8,log=True,color='b',alpha=0.4)
    xs = bins[:-1]+np.diff(bins)/2
    smooth_ys = np.array([np.power(10,np.mean(np.log10(0.2+ys[max(0,i-3):min(len(ys),i+4)]))) for i in range(len(ys))])
    smoother_ys = np.array([np.mean(ys[max(0,i-12):min(len(ys),i+13)]) for i in range(len(ys))])
    ax.plot(xs[2:81],smooth_ys[2:81],alpha=0.7,c='k')
    ax.plot(xs[80:120],smooth_ys[80:120],alpha=0.7,c='k',linestyle='--')
    ax.grid(True)
    plt.show()

def each_cluster_size_against_diameter_plot(clusters,surveys):
    cols = ['#008080',
            '#03396c',
            '#a40b0b',
            '#f36b2c',
            '#e39cf7',
            '#9e379f' ]

    diams = [[] for i in range(6)]
    for tile_clusters,tile_surveys in zip(clusters,surveys):
        for n in range(1,7):
            centres_on_tile_of_size = convert.clusters2np([tile_clusters[i] for i in range(len(tile_clusters)) if len(tile_clusters[i])==n],tile_surveys)
            diams[n-1] += list(centres_on_tile_of_size[:,2])

    fig,ax = plt.subplots()
    diams = [diams[0],diams[1]+diams[2],diams[3]+diams[4],diams[5]]
    for n in range(len(diams)):
        ys,bins,patches = ax.hist(diams[n],[i for i in range(180)],rwidth=0.8,log=True,color=cols[n],alpha=0.)
        xs = bins[:-1]+np.diff(bins)/2
        smooth_ys = np.array([np.power(10,np.mean(np.log10(0.2+ys[max(0,i-3):min(len(ys),i+4)]))) for i in range(len(ys))])
        smoother_ys = np.array([np.mean(ys[max(0,i-12):min(len(ys),i+13)]) for i in range(len(ys))])
        ax.plot(xs[2:81],smooth_ys[2:81],alpha=0.8,c=cols[n])
        ax.plot(xs[80:120],smooth_ys[80:120],alpha=0.7,c=cols[n],linestyle='--')
    ax.grid(True)
    plt.show()


if __name__=='__main__':
    import sys
    import matplotlib.pyplot as plt


    xml_master_dir = sys.argv[1]
    dfs = load_all_surveys(xml_master_dir)[1:4]

    ###GLOBAL STUFF
    # individual_annotation_size_plot(dfs)

    ###CLUSTERING
    nodes = calc_all_nodetrees(dfs,distance.negative_jaccard)
    d=0.8
    clusters = []
    for nodes_in_tile in nodes:
        clusters.append(cluster_surveys.clusters_at_distance(nodes_in_tile,d))
    each_cluster_size_against_diameter_plot(clusters,dfs)
    # dists = [0.+0.99*i for i in range(10)]
    # clusters = []
    # n_clusters = np.empty([len(dists),len(nodes)])
    # n_singles = np.empty([len(dists),len(nodes)])
    # n_multi = np.empty([len(dists),len(nodes)])
    #



    # for i,d in enumerate(dists):
    #     clusters_at_d = []
    #     diameters_at_d = []
    #     for j,tile in enumerate(nodes):
    #         clusters_at_d_on_tile = cluster_surveys.clusters_at_distance(tile,d)
    #         clusters_at_d.append(clusters_at_d_on_tile)
    #         centres = convert.clusters2np(clusters_at_d_on_tile,dfs[j])
    #         n_clusters[i,j] = len(clusters_at_d[j])
    #         n_singles[i,j] = len([c for c in clusters_at_d[j] if len(c)==1])
    #         n_multi[i,j] = len([c for c in clusters_at_d[j] if len(c)>1])
    #         diameters_at_d += list(centres[:,2])
    #     fig,ax=plt.subplots()
    #     ax.hist(diameters_at_d,[i for i in range(150)],rwidth=0.8,log=True)
    #     ax.grid(True)
    #     plt.show()
    #     clusters.append(clusters_at_d)
    #
    # print(np.array(n_clusters))
    #
    # fig,ax = plt.subplots()
    # hists = []
    # for d,cluster_set in zip(dists,clusters):
    #     hists.append(np.zeros(6))
    #     for tile in cluster_set:
    #         cluster_sizes = [len(cluster) for cluster in tile]
    #         this_hist,_ = np.histogram(cluster_sizes,bins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5])
    #         # print(this_hist)
    #         hists[-1] = hists[-1] + this_hist
    #         # print(hists[-1])
    #     ax.semilogy([1,2,3,4,5,6],hists[-1])
    #     print(hists[-1])
    # plt.show()
    #
    # xml_dir = sys.argv[1]
    # img_path = sys.argv[2]
    # img_dir,img_name = os.path.split(img_path)
    # d = 0.95
    # df = [convert.xml2df(os.path.join(xml_dir,s_i)) for s_i in os.listdir(xml_dir)]
    # nodes = cluster_surveys.agglomerative(df,distance.negative_jaccard)
    # clusters = cluster_surveys.clusters_at_distance(nodes,d)
    # xml_out = convert.clusters2PASCAL_VOC(clusters,df,img_name,out_dir=img_dir)
