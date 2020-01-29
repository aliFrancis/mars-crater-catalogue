import numpy as np
import pandas as pd
import seaborn as sn


def total_binary_IOU(paths):
    binary_IOU_mat = binary_IOU_matrix(paths,plot=True)
    binary_IOU = (np.sum(binary_IOU_mat)-len(paths))/(np.size(binary_IOU_mat)-len(paths))
    return binary_IOU

def total_IOU(paths):
    IOU_mat = IOU_matrix(paths,plot=True)
    IOU = (np.sum(IOU_mat)-len(paths))/(np.size(IOU_mat)-len(paths))
    return IOU

def binary_IOU_matrix(paths, plot = False):
    survey_names = [s_i.replace('.xml','')[-6:] for s_i in paths]
    surveys = [convert.xml2df(s_i) for s_i in paths]


    binary_IOU_mat = np.empty((len(surveys),len(surveys)))
    for i,s_i in enumerate(surveys):
        for j,s_j in enumerate(surveys):
            if j>i:
                iou_ij = iou.all_ious(s_i,s_j)
                iou_max_i = np.max(iou_ij,axis=1)
                iou_max_j = np.max(iou_ij,axis=0)
                binary_IOU_i = iou_max_i>=0.5
                binary_IOU_j = iou_max_j>=0.5
                binary_IOU_mat[i,j] = np.mean(binary_IOU_i)
                binary_IOU_mat[j,i] = np.mean(binary_IOU_j)
            if j==i:
                binary_IOU_mat[i,i] = 1

    if plot:
        df_agreement = pd.DataFrame(binary_IOU_mat, index = survey_names,
          columns = survey_names)
        plt.figure(figsize=(10,7))
        plt.title('AVERAGE BINARY IOU')
        sn.heatmap(df_agreement,annot=True,vmin=0,vmax=1)
        plt.show()
    return binary_IOU_mat

def IOU_matrix(paths, plot = False):
    survey_names = [s_i.replace('.xml','')[-6:] for s_i in paths]
    surveys = [convert.xml2df(s_i) for s_i in paths]

    IOU_mat = np.empty((len(surveys),len(surveys)))
    for i,s_i in enumerate(surveys):
        for j,s_j in enumerate(surveys):
            if j>i:
                iou_ij = iou.all_ious(s_i,s_j)
                iou_max_i = np.max(iou_ij,axis=1)
                iou_max_j = np.max(iou_ij,axis=0)
                IOU_mat[i,j] = np.mean(iou_max_i)
                IOU_mat[j,i] = np.mean(iou_max_j)
            if j==i:
                IOU_mat[i,i] = 1


    if plot:
        df_agreement = pd.DataFrame(IOU_mat, index = survey_names,
        columns = survey_names)
        plt.figure(figsize=(10,7))
        plt.title('AVERAGE MAX IOU')
        sn.heatmap(df_agreement,annot=True,vmin=0,vmax=1)
        plt.show()
    return IOU_mat

if __name__ == '__main__':
    import os
    import sys

    import iou
    from data import convert
    import matplotlib.pyplot as plt

    survey_dir = sys.argv[1]
    surveys = [os.path.join(survey_dir,path) for path in os.listdir(survey_dir)]
    print(total_binary_IOU(surveys))
    print(total_IOU(surveys))
