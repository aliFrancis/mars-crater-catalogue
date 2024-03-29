import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

def iou(crater1,crater2):
    """
    Calculates amount of overlap as fraction of total union area of two craters
    """
    if isinstance(crater1,type(pd.DataFrame())):
        x1 = crater1['x']
        y1 = crater1['y']
        D1 = crater1['D']
    elif isinstance(crater1,type(np.ndarray(None))):
        [x1,y1,D1] = crater1[2:5].astype(float)
    elif isinstance(crater1,(list,tuple)):
        [x1,y1,D1] = np.array(crater1[0:3]).astype(float)
    r1 = D1/2
    if isinstance(crater2,type(pd.DataFrame())):
        [x2,y2,D2] = crater2.values.astype(float)
    elif isinstance(crater2,type(np.ndarray(None))):
        [x2,y2,D2] = crater2[2:5].astype(float)
    elif isinstance(crater2,(list,tuple)):
        [x2,y2,D2] = np.array(crater2[0:3]).astype(float)
    r2 = D2/2

    d = np.sqrt(np.square((x1-x2))+np.square((y1-y2)))

    if x1==x2 and y1==y2 and r1==r2:
        return 1
    elif d<abs(r1-r2):
        A = np.pi*np.square(min(r1,r2))
    elif d<r1+r2:
        A = np.square(r1)*np.arccos((np.square(d)+np.square(r1)-np.square(r2))/(2*d*r1)) + \
            np.square(r2)*np.arccos((np.square(d)+np.square(r2)-np.square(r1))/(2*d*r2)) - \
            (1/2)*np.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))
    else:
        A = 0

    return A/(np.pi*np.square(r1)+np.pi*np.square(r2)-A)


def all_ious(survey1,survey2):
    """
    Calculates IOU between each entry in two surveys, returning as matrix
    """
    if isinstance(survey1,type(pd.DataFrame())):
        survey1 = survey1.values
    if isinstance(survey2,type(pd.DataFrame())):
        survey2 = survey2.values

    results = np.empty([survey1.shape[0],survey2.shape[0]])
    for i,survey1_i in enumerate(survey1):
        for j,survey2_j in enumerate(survey2):
            results[i,j] = iou(survey1_i,survey2_j)
    return results

def all_ious_np(survey1,survey2):
    """
    Calculates IOU between each entry in two surveys, returning as matrix, using cdist
    """
    if isinstance(survey1,type(pd.DataFrame())):
        survey1 = survey1.values
    if isinstance(survey2,type(pd.DataFrame())):
        survey2 = survey2.values

    results = cdist(survey1,survey2,metric=iou)
    return results
