import os
import numpy as np

from utils import convert

if __name__=='__main__':
    clustered_dir = os.path.join(__file__,'../..','data/annotations/clustered')
    surveys=[]
    for path in os.listdir(clustered_dir):
        surveys.append(convert.xml2df(os.path.join(clustered_dir,path)))
        print(
            path+':',
            '  individual count -', np.sum(surveys[-1]['conf']),
            '  count -', len(surveys[-1]),
            '  confidence mean - ', np.round(np.mean(surveys[-1]['conf']),2),
            '  median -', np.median(surveys[-1]['D']*6),
            '  mean -', np.round(np.mean(surveys[-1]['D'])*6,2),
            )

    allsurveys = convert.dfs2df(surveys)
    print(
        '      TOTAL:',
        '  individual count -', np.sum(allsurveys['conf']),
        '  count -', len(allsurveys),
        '  confidence mean - ', np.round(np.mean(allsurveys['conf']),2),
        '  median -', np.median(allsurveys['D']*6),
        '  mean -', np.round(np.mean(allsurveys['D'])*6,2),
        )
