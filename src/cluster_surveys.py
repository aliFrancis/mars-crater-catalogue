from scipy.cluster.hierarchy import linkage, dendrogram, to_tree
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from data import convert
import distance


def clusters_at_distance(nodelist,max_distance):
    found_leaves = []
    clusters = []
    dists = np.array([nodelist[i].dist for i in range(len(nodelist))])
    try:
        curr_id = np.max(np.where(dists<=max_distance))
    except ValueError: #no dists<=max_distance
        curr_id = 0
    while curr_id > 0:
        curr_node = nodelist[curr_id]
        curr_node_leaves = get_node_leaves(curr_node)
        if not any(curr_leaf in found_leaves for curr_leaf in curr_node_leaves):
            clusters.append(curr_node_leaves)
            found_leaves+=curr_node_leaves
        curr_id-=1
    return clusters

def get_node_leaves(node,leaves=[],init=True):
    if init:
        leaves = []
    if node.left is None:
        leaves.append(node.id)
    else:
        leaves = get_node_leaves(node.left,leaves=leaves,init=False)
        leaves = get_node_leaves(node.right,leaves=leaves,init=False)
    return sorted(leaves)

def agglomerative(surveys,dist_metric):
    if isinstance(surveys,list) or isinstance(surveys,pd.DataFrame):
        surveys,table = convert.df2np(surveys)
    N = surveys.shape[0]
    dist_mat = pdist(surveys,metric=dist_metric)
    linkage_mat = linkage(dist_mat,method='average',metric=dist_metric)
    rootnode, nodelist = to_tree(linkage_mat,rd=True)
    return nodelist


if __name__=='__main__':
    import sys
    import os

    xml_dir = sys.argv[1]
    assert os.path.isdir(xml_dir), 'xml_dir is not a directory!'
    dfs = [convert.xml2df(os.path.join(xml_dir,s_i)) for s_i in os.listdir(xml_dir)]
    nodes = agglomerative(dfs, distance.scaled_3D)
