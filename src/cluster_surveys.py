from scipy.cluster.hierarchy import linkage, dendrogram, to_tree
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils import convert, distance


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
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Combines annotations across whole dataset using agglomerative clustering.')
    parser.add_argument('annotation_dir', help='Directory with xml files')
    parser.add_argument('output_dir', help='Directory for outputted xmls')
    parser.add_argument('-d','--distance_metric', type=str, help='Distance function (defined in distance.py)', default=distance.negative_jaccard)
    parser.add_argument('-t','--threshold', type=float, help='Distance threshold at which to cluster', default=0.9)
    args = vars(parser.parse_args())

    annotation_dir = args['annotation_dir']
    output_dir  = args['output_dir']
    distance_metric = args['distance_metric']
    if isinstance(distance_metric,str):
        try:
            distance_metric = getattr(distance,distance_metric)
        except AttributeError:
            'distance metric not recognised'
    threshold = args['threshold']

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    annotation_register = {}
    for root,dirs,paths in os.walk(annotation_dir):
        for path in paths:
            if path.endswith('.xml'):
                image = os.path.basename(root)
                if not image in annotation_register.keys():
                    annotation_register[image] = [os.path.join(root,path)]
                else:
                    annotation_register[image].append(os.path.join(root,path))
    for image_name,files in annotation_register.items():
        df = [convert.xml2df(file) for file in files]
        nodes = agglomerative(df,distance.negative_jaccard)
        clusters = clusters_at_distance(nodes,threshold)
        xml_out = convert.clusters2PASCAL_VOC(clusters,df,image_name,out_dir=output_dir)
