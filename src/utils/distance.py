import math

def flat_2D(point1,point2):
    if point1[0] == point2[0]:
        return 999999999.
    else:
        return math.sqrt((point1[2]-point2[2])**2 + (point1[3]-point2[3])**2)

def flat_3D(point1,point2):
    if point1[0] == point2[0]:
        return 999999999.
    else:
        return math.sqrt((point1[2]-point2[2])**2 + (point1[3]-point2[3])**2 + (point1[4]-point2[4])**2)

def scaled_2D(point1,point2):
    """
    Euclidean distance of centres, scaled by average of the two diameters, so that smaller craters appear further away
    """
    if point1[0] == point2[0]:
        return 999999999.
    else:
        return 1/((point1[4]+point2[4])/2)*math.sqrt((point1[2]-point2[2])**2 + (point1[3]-point2[3])**2)

def scaled_3D(point1,point2):
    """
    Euclidean distance including diameter, scaled by average of the two diameters, so that smaller craters appear further away
    """
    if point1[0] == point2[0]:
        return 999999999.
    else:
        return 1/((point1[4]+point2[4])/2)*math.sqrt((point1[2]-point2[2])**2 + (point1[3]-point2[3])**2 + (point1[4]-point2[4])**2)

def negative_jaccard(point1,point2):
    """
    Calculates (1 - amount) of overlap as fraction of total union area of two craters
    """
    if point1[0] == point2[0]:
        return 999999999.

    x1,y1,D1 = point1[2:5]
    x2,y2,D2 = point2[2:5]
    r1 = D1/2
    r2 = D2/2
    d = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

    if x1==x2 and y1==y2 and r1==r2:
        return 0
    elif d<abs(r1-r2):
        A = math.pi*math.pow(min(r1,r2),2)
    elif d<r1+r2:
        A = math.pow(r1,2)*math.acos((math.pow(d,2)+math.pow(r1,2)-math.pow(r2,2))/(2*d*r1)) + \
            math.pow(r2,2)*math.acos((math.pow(d,2)+math.pow(r2,2)-math.pow(r1,2))/(2*d*r2)) - \
            (1/2)*math.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))
    else:
        return 1

    return 1 - A/(math.pi*math.pow(r1,2)+math.pi*math.pow(r2,2)-A)



def negative_jaccard_with_diameter_priority(point1,point2):
    """
    Calculates (1 - amount) of overlap as fraction of total union area of two craters,
    then multiplies by relative size difference of circles.
    """
    if point1[0] == point2[0]:
        return 999999999.

    x1,y1,D1 = point1[2:5]
    x2,y2,D2 = point2[2:5]
    r1 = D1/2
    r2 = D2/2
    d = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

    size_ratio = max(r1/r2,r2/r1)

    if x1==x2 and y1==y2 and r1==r2:
        return 0
    elif d<abs(r1-r2):
        A = math.pi*math.pow(min(r1,r2),2)
    elif d<r1+r2:
        A = math.pow(r1,2)*math.acos((math.pow(d,2)+math.pow(r1,2)-math.pow(r2,2))/(2*d*r1)) + \
            math.pow(r2,2)*math.acos((math.pow(d,2)+math.pow(r2,2)-math.pow(r1,2))/(2*d*r2)) - \
            (1/2)*math.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))
    else:
        return size_ratio

    return size_ratio*(1 - A/(math.pi*math.pow(r1,2)+math.pi*math.pow(r2,2)-A))

def negative_jaccard_plus_distance(point1,point2):
    """
    Calculates (1 - amount) of overlap as fraction of total union area of two craters, if overlap is
    zero then distance defined by flat_2D distance between centres, normalised by (r1+r2)
    """
    if point1[0] == point2[0]:
        return 999999999.

    x1,y1,D1 = point1[2:5]
    x2,y2,D2 = point2[2:5]
    r1 = D1/2
    r2 = D2/2
    d = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

    if x1==x2 and y1==y2 and r1==r2:
        return 0
    elif d<abs(r1-r2):
        A = math.pi*math.pow(min(r1,r2),2)
    elif d<r1+r2:
        A = math.pow(r1,2)*math.acos((math.pow(d,2)+math.pow(r1,2)-math.pow(r2,2))/(2*d*r1)) + \
            math.pow(r2,2)*math.acos((math.pow(d,2)+math.pow(r2,2)-math.pow(r1,2))/(2*d*r2)) - \
            (1/2)*math.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))
    else:
        return flat_2D(point1,point2)/(r1+r2)

    return 1 - A/(math.pi*math.pow(r1,2)+math.pi*math.pow(r2,2)-A)
