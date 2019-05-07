"""
script to take a LabelImg output xml, and the set of craters it corresponds to,
and make an array documenting TP and FP craters with their localisation errors.
"""
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import sys
from skimage.io import imread
import ast



def surveyxml2df(xml_path,surveyor=None, out_csv_path=None, min_D = 0, max_D = float('inf')):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if surveyor==None:
        surveyor = xml_path

    d = {'surveyor':[],'ID':[],'x':[],'y':[],'D':[],'diff':[]}
    df = pd.DataFrame(data = d)
    i = 0
    for child in root:
        if child.tag == 'object':
            for grandchild in child:
                if grandchild.tag == 'difficult':
                    diff = int(grandchild.text)
                if grandchild.tag == 'bndbox':

                    ymin = float(grandchild[0].text)
                    xmin = float(grandchild[1].text)
                    ymax = float(grandchild[2].text)
                    xmax = float(grandchild[3].text)

                    x = (xmin+xmax)/2
                    y = (ymin+ymax)/2
                    D = xmax-xmin
                    D_ = ymax-ymin
                    if min_D < D and D < max_D:
                        i+=1
                        df_line = pd.DataFrame(data = {'surveyor':[surveyor],'ID':[str(i).zfill(4)],'x':[x],'y':[y],'D':[D],'diff':[diff]})
                        df = pd.concat((df,df_line))

    if out_csv_path:
        df.to_csv(out_csv_path)
    return df


if __name__=='__main__':
    #import survey as numpy array
    import os
    import argparse
    import display_surveys as disp

    
    parser = argparse.ArgumentParser(description='Converts many xml annotations into single pandas DataFrame, then displays')
    parser.add_argument('img_path', help='Path to image file')
    parser.add_argument('xml_dir', help='Path to directory with xml files')
    parser.add_argument('-c','--contrast',type=float, help='Factor for contrast readjustment', default=1.)
    parser.add_argument('-a','--alpha', type=float,help='Opacity of annotations in plot', default=0.5)
    args = vars(parser.parse_args())
    img_path = args['img_path']
    xml_dir  = args['xml_dir']
    contrast = args['contrast']
    alpha    = args['alpha']

    img = imread(img_path)

    dfs = []
    if os.path.isfile(xml_dir):
        dfs = [surveyxml2df(xml_dir)]
    else:
        dfs = [surveyxml2df(s_i) for s_i in os.listdir(xml_dir)]
    disp.display_surveys(img,dfs,contrast_factor=contrast,alpha=alpha)
