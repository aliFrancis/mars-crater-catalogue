import os
import numpy as np

from utils import convert

if __name__=='__main__':
    clustered_dir = os.path.join(os.path.dirname(__file__),'..','data/annotations/clustered')
    surveys=[]
    for path in os.listdir(clustered_dir):
        surveys.append(convert.xml2df(os.path.join(clustered_dir,path)))
        print(
            path+':',
            ' individual count -', str(np.sum(surveys[-1]['conf']).astype(int)).ljust(5),
            ' count -', str(len(surveys[-1])).ljust(5),
            ' conf. mean - ', str(np.round(np.mean(surveys[-1]['conf']),2)).ljust(5),
            ' diam. median -', str(np.median(surveys[-1]['D']*6)).ljust(5)+'m',
            ' diam. mean -', str(np.round(np.mean(surveys[-1]['D'])*6,2)).ljust(5)+'m',
            ' diam. min -', str(np.round(np.min(surveys[-1]['D'])*6,2)).ljust(5)+'m',
            ' diam. max -', str(np.round(np.max(surveys[-1]['D'])*6,2)).ljust(5)+'m',
            )

    allsurveys = convert.dfs2df(surveys)
    print(
        '      TOTAL:',
        ' individual count -', str(np.sum(allsurveys['conf']).astype(int)).ljust(5),
        ' count -', str(len(allsurveys)).ljust(5),
        ' conf. mean - ', str(np.round(np.mean(allsurveys['conf']),2)).ljust(5),
        ' diam. median -', str(np.median(allsurveys['D']*6)).ljust(5)+'m',
        ' diam. mean -', str(np.round(np.mean(allsurveys['D'])*6,2)).ljust(5)+'m',
        ' diam. min -', str(np.round(np.min(allsurveys['D'])*6,2)).ljust(5)+'m',
        ' diam. max -', str(np.round(np.max(allsurveys['D'])*6,2)).ljust(5)+'m',
        )
