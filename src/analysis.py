import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

from utils import convert, iou


def average_pairwise_IOU(IOU_mat):
    n = IOU_mat.shape[0]
    mean_IOU = (np.sum(IOU_mat)-n)/(np.size(IOU_mat)-n)
    return mean_IOU

def pairwise_IOU_matrices(paths, plot = False):
    survey_names = [p.replace('.xml','')[-6:] for p in paths]
    surveys = [convert.xml2df(p) for p in paths]
    binary_IOU_mat = np.empty((len(surveys),len(surveys)))
    IOU_mat = np.empty((len(surveys),len(surveys)))
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
                IOU_mat[i,j] = np.mean(iou_max_i)
                IOU_mat[j,i] = np.mean(iou_max_j)
            if j==i:
                binary_IOU_mat[i,i] = 1
                IOU_mat[i,i] = 1

    if plot:
        df_agreement = pd.DataFrame(binary_IOU_mat, index = survey_names,
          columns = survey_names)
        plt.figure(figsize=(10,7))
        plt.title('AVERAGE BINARY IOU')
        sn.heatmap(df_agreement,annot=True,vmin=0,vmax=1)
        plt.show()

        df_agreement = pd.DataFrame(IOU_mat, index = survey_names,
        columns = survey_names)
        plt.figure(figsize=(10,7))
        plt.title('AVERAGE MAX IOU')
        sn.heatmap(df_agreement,annot=True,vmin=0,vmax=1)
        plt.show()
    return binary_IOU_mat, IOU_mat

def group_IOU_matrices(paths):
    survey_names = [p.replace('.xml','')[-6:] for p in paths]
    surveys = [convert.xml2df(p) for p in paths]
    binary_IOUs = []
    IOUs = []
    for i,s_i in enumerate(surveys):
        iou_i = []
        for j,s_j in enumerate(surveys):
            if j!=i:
                iou_i.append(iou.all_ious(s_i,s_j))
        iou_i = np.concatenate(iou_i,axis=1)
        iou_max_i = np.max(iou_i,axis=1)
        binary_IOU_i = iou_max_i>=0.5
        binary_IOUs.append(np.mean(binary_IOU_i))
        IOUs.append(np.mean(iou_max_i))

    return binary_IOUs, IOUs

if __name__ == '__main__':
    import os
    import sys

    survey_dir = sys.argv[1]
    paths = [os.path.join(survey_dir,path) for path in os.listdir(survey_dir)]
    surveys = [convert.xml2df(p) for p in paths]
    print('\nANALYSIS OF {}'.format(os.path.basename(survey_dir)),'\n')
    print(' NO. OF ANNOTATIONS')
    print(' ------------------')
    for survey,path in zip(surveys,paths):
        print(' ',os.path.basename(path).replace('.xml','')+':',len(survey))
    total_survey = convert.dfs2df(surveys)
    print('  ____________')
    print('  TOTAL :',len(total_survey))
    print('\n')

    group_binary_IOUs, group_IOUs = group_IOU_matrices(paths)
    print('GROUP BINARY')
    print(group_binary_IOUs)
    print(np.mean(group_binary_IOUs))
    print('GROUP MEAN')
    print(group_IOUs)
    print(np.mean(group_IOUs))
