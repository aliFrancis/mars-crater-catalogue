import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import sys
from skimage.io import imread
import ast
import numpy as np
import math


def xml2df(xml_path,surveyor=None, out_csv_path=None, min_D = 0, max_D = float('inf')):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if surveyor==None:
        surveyor = xml_path

    d = {'surveyor':[],'ID':[],'x':[],'y':[],'D':[],'diff':[],'conf':[]}
    df = pd.DataFrame(data = d)
    i = 0
    for child in root:
        if child.tag == 'object':
            diff = None
            conf = None
            for grandchild in child:
                if grandchild.tag == 'difficult':
                    diff = int(grandchild.text)
                if grandchild.tag == 'confidence':
                    conf = int(grandchild.text)
                if grandchild.tag == 'bndbox':

                    ymin = float(grandchild[0].text)
                    xmin = float(grandchild[1].text)
                    ymax = float(grandchild[2].text)
                    xmax = float(grandchild[3].text)

                    x = (xmin+xmax)/2
                    y = (ymin+ymax)/2
                    D = xmax-xmin
                    D_ = ymax-ymin
            if min_D <= D and D <= max_D:
                i+=1
                df_line = pd.DataFrame(data = {
                                        'surveyor':[surveyor],
                                        'ID':[str(i).zfill(4)],
                                        'x':[x],
                                        'y':[y],
                                        'D':[D],
                                        'diff':[diff],
                                        'conf':[conf]
                                        })
                df = pd.concat((df,df_line))
    df = df[['surveyor','ID','x','y','D','diff','conf']]
    if all(d is None for c in df['diff']):
        del df['diff']
    if all(c is None for c in df['conf']):
        del df['conf']
    if out_csv_path:
        df.to_csv(out_csv_path)
    return df

def dfs2df(dfs):
    return pd.concat(dfs,ignore_index=True)

def clusters2np(clusters,surveys):
    if isinstance(surveys,list) or isinstance(surveys,pd.DataFrame):
        surveys,_ = df2np(surveys)
    rep = []
    for cluster in clusters:
        cluster_points = surveys[cluster,...]
        x = np.mean(cluster_points[:,2])
        y = np.mean(cluster_points[:,3])
        D = np.mean(cluster_points[:,4])
        N = len(cluster)
        rep.append([x,y,D,N])

    return np.array(rep)

def df2np(df):
    if isinstance(df,list):
        df = pd.concat(df)

    surveyor_list = np.unique(df.surveyor.values)
    surveyor_table = dict()
    for i,surveyor in enumerate(surveyor_list):
        surveyor_table[surveyor] = i

    d = {'surveyor':[],'ID':[],'x':[],'y':[],'D':[],'diff':[]}

    arr = df.values
    for i in range(len(arr)):
        arr[i][0] = surveyor_table[arr[i][0]]
    arr = arr.astype(np.float)
    return arr,surveyor_table


def clusters2PASCAL_VOC(clusters,surveys,img_name,out_dir=None):
    """
    Converts list of clusters and parent image into an xml, in pascal VOC format
    """
    if isinstance(surveys,list) or isinstance(surveys,pd.DataFrame):
        surveys,surveyors = df2np(surveys)

    annotation = ET.Element('annotation')
    filename = ET.SubElement(annotation,'filename')
    source = ET.SubElement(annotation,'source')
    so_database = ET.SubElement(source,'database')
    so_annotation = ET.SubElement(source,'annotation')
    so_image = ET.SubElement(source,'image')

    size = ET.SubElement(annotation,'size')
    si_width = ET.SubElement(size,'width')
    si_height = ET.SubElement(size,'height')
    si_depth = ET.SubElement(size,'depth')

    segmented = ET.SubElement(annotation,'segmented')

    filename.text = img_name
    so_database.text = 'MSSL ORBYTS MCC'
    so_annotation.text = 'MSSL ORBYTS'
    so_image.text = 'NASA CTX / iMars'

    si_width.text = '2000'
    si_height.text = '2000'
    si_depth.text = '1'

    segmented.text = '0'

    cluster_vals = clusters2np(clusters,surveys)
    for i,cluster in enumerate(clusters):
        object = ET.SubElement(annotation,'object')
        name = ET.SubElement(object,'name')
        pose = ET.SubElement(object,'pose')
        truncated = ET.SubElement(object,'truncated')
        occluded = ET.SubElement(object,'occluded')
        bndbox = ET.SubElement(object,'bndbox')
        xmin = ET.SubElement(bndbox,'xmin')
        ymin = ET.SubElement(bndbox,'ymin')
        xmax = ET.SubElement(bndbox,'xmax')
        ymax = ET.SubElement(bndbox,'ymax')
        difficult = ET.SubElement(object,'difficult')
        confidence = ET.SubElement(object,'confidence')

        y_centre,x_centre,D,N = cluster_vals[i,...]

        xmin_val = int(round(x_centre-0.5*D))
        ymin_val = int(round(y_centre-0.5*D))
        xmax_val = int(round(x_centre+0.5*D))
        ymax_val = int(round(y_centre+0.5*D))

        name.text = 'crater'
        pose.text = 'frontal'
        truncated.text = '0'
        occluded.text = '0'
        xmin.text = str(xmin_val)
        ymin.text = str(ymin_val)
        xmax.text = str(xmax_val)
        ymax.text = str(ymax_val)
        difficult.text = str(int(N==1)) #Marked difficult if only one annotator in cluster
        confidence.text = str(len(cluster))


    data = minidom.parseString(ET.tostring(annotation,encoding='unicode')).toprettyxml(indent="  ")
    if out_dir is None:
        xmlfile = open("{}.xml".format(img_name), "w")
    else:
        xmlfile = open("{}/{}.xml".format(out_dir,img_name), "w")
    xmlfile.write(str(data))
    return data
