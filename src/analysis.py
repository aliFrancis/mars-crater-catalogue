import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

from utils import convert, iou


def average_pairwise_IOU(IOU_mat):
    n = IOU_mat.shape[0]
    mean_IOU = (np.sum(IOU_mat)-n)/(np.size(IOU_mat)-n)
    return mean_IOU

def group_IOU_matrices(paths):
    survey_names = [p.replace('.xml','')[-6:] for p in paths]
    surveys = [convert.xml2df(p) for p in paths]
    binary_IOUs = []
    IOUs = []
    for i,s_i in enumerate(surveys):
        iou_i = []
        for j,s_j in enumerate(surveys):
            if j!=i:
                iou_i.append(iou.all_ious_np(s_i,s_j))
        iou_i = np.concatenate(iou_i,axis=1) #Compare 1 person's annotations to everyone else's
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
    print(' MEAN IoU')
    print(' --------')
    for i,path in enumerate(paths):
        print(' ',os.path.basename(path).replace('.xml','')+':',np.round(group_IOUs[i],4))
    print('  ____________')
    print('   MEAN :',np.round(np.mean(group_IOUs),4))
    print('\n')

    print('\n MEAN BINARY IoU (IoU treated as 1 if above 0.5)')
    print(' -----------------------------------------------')
    for i,path in enumerate(paths):
        print(' ',os.path.basename(path).replace('.xml','')+':',np.round(group_binary_IOUs[i],4))
    print('  ____________')
    print('   MEAN :',np.round(np.mean(group_binary_IOUs),4))
    print('\n')
