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

if __name__=='__main__':
    import sys
    import matplotlib.pyplot as plt


    xml_master_dir = sys.argv[1]
    dfs = load_all_surveys(xml_master_dir)
    nodes = calc_all_nodetrees(dfs,distance.negative_jaccard)

    dists = [0.7+0.01*i for i in range(30)]
    clusters = []
    n_clusters = np.empty([len(dists),len(nodes)])
    n_singles = np.empty([len(dists),len(nodes)])
    n_multi = np.empty([len(dists),len(nodes)])

    for i,d in enumerate(dists):
        clusters_at_d = []
        for j,tile in enumerate(nodes):
            clusters_at_d.append(cluster_surveys.clusters_at_distance(tile,d))
            n_clusters[i,j] = len(clusters_at_d[j])
            n_singles[i,j] = len([c for c in clusters_at_d[j] if len(c)==1])
            n_multi[i,j] = len([c for c in clusters_at_d[j] if len(c)>1])

        clusters.append(clusters_at_d)

    # print(np.array(n_clusters))

    fig,ax = plt.subplots()
    hists = []
    for d,cluster_set in zip(dists,clusters):
        hists.append(np.zeros(6))
        for tile in cluster_set:
            cluster_sizes = [len(cluster) for cluster in tile]
            this_hist,_ = np.histogram(cluster_sizes,bins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5])
            # print(this_hist)
            hists[-1] = hists[-1] + this_hist
            # print(hists[-1])
        ax.semilogy([1,2,3,4,5,6],hists[-1])
        print(hists[-1])
    plt.show()
