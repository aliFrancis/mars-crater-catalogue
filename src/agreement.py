import numpy as np
import pandas as pd
import seaborn as sn


def





if __name__ == '__main__':
    import os
    import sys

    import iou
    from data import convert
    import matplotlib.pyplot as plt

    survey_dir = sys.argv[1]
    surveys = [os.path.join(survey_dir,path) for path in os.listdir(survey_dir)]
    survey_names = [s_i[-6:] for s_i in surveys]
    surveys = [convert.xml2df(s_i) for s_i in surveys]
    for id,survey in zip(survey_names,surveys):
        print('{:>8}: {:>5}'.format(id,len(survey)))


    agreement_mat = np.empty((len(surveys),len(surveys)))
    binary_mat    = np.empty((len(surveys),len(surveys)))
    print('\n')
    for i,s_i in enumerate(surveys):
        for j,s_j in enumerate(surveys):
            if j>=i:
                print(survey_names[i],survey_names[j],end='\r')
                iou_ij = iou.all_ious(s_i,s_j)
                iou_max_i = np.max(iou_ij,axis=1)
                iou_max_j = np.max(iou_ij,axis=0)
                binary_i = iou_max_i>=0.5
                binary_j = iou_max_j>=0.5
                agreement_mat[i,j] = np.mean(iou_max_i)
                agreement_mat[j,i] = np.mean(iou_max_j)
                binary_mat[i,j]    = np.mean(binary_i)
                binary_mat[j,i]    = np.mean(binary_j)

    df_agreement = pd.DataFrame(agreement_mat, index = survey_names,
      columns = survey_names)
    df_binary    = pd.DataFrame(binary_mat   , index = survey_names,
      columns = survey_names)
    plt.figure(figsize=(10,7))
    plt.title('AVERAGE MAX IOU')
    sn.heatmap(df_agreement,annot=True,vmin=0,vmax=1)
    plt.figure(figsize=(10,7))
    plt.title('MAX IOU>0.5')
    sn.heatmap(df_binary,annot=True,vmin=0,vmax=1)
    plt.show()
    print(agreement_mat)
