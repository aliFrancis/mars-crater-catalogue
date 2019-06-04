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

    xml_master_dir = sys.argv[1]
    dfs = load_all_surveys(xml_master_dir)
    nodes = calc_all_nodetrees(dfs,distance.negative_jaccard_with_diameter_priority)

    dists = [0.4+0.1*i for i in range(6)]
    clusters = []
    n_clusters = np.empty([len(dists),len(nodes)])
    for i,d in enumerate(dists):
        clusters_at_d = []
        for j,tile in enumerate(nodes):
            clusters_at_d.append(cluster_surveys.clusters_at_distance(tile,d))
            n_clusters[i,j] = len(clusters_at_d[j])
            print(n_clusters)
        clusters.append(clusters_at_d)


    print(clusters)
    print(n_clusters)
