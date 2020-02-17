import matplotlib.pyplot as plt
import os
from matplotlib.collections import EllipseCollection



def display_surveys(img,surveys,contrast_factor=None,alpha=0.3,plotting=True):
    fig,ax=plt.subplots()
    if contrast_factor is not None:
        img = img.astype('float')
        img = (img-img.mean())*contrast_factor/(img.max()-img.min())+0.4
        ax.imshow(img,cmap='gray',vmin=0,vmax=1)
    else:
        ax.imshow(img,cmap='gray')
    cols = ['tab:red','tab:blue','tab:green','tab:cyan','tab:orange','tab:olive','tab:brown']
    ecs=[]
    for ind,survey in enumerate(surveys):
        colour = cols[ind]
        ec = EllipseCollection(widths=survey['D'].values,heights=survey['D'].values,angles=0,units='xy',
                                offsets = list(zip(survey['y'].values,survey['x'].values)),
                                transOffset=ax.transData,facecolors='None',edgecolors = colour,linewidth=1.5,
                                alpha=alpha)
        ecs.append(ec)
        if plotting:
            ax.add_collection(ec)
            print('{:>7}: {:>8} - {} markings'.format(os.path.split(survey['surveyor'].values[0])[-1],colour[4:],len(survey['D'].values)))

    if plotting:
        fig.tight_layout()
        plt.show(block=True)
    else:
        return ecs


if __name__=='__main__':
    #import survey as numpy array
    import os
    import sys
    from skimage.io import imread
    import convert


    img_path = sys.argv[1]
    img = imread(img_path)
    xml_dir = sys.argv[2]

    if len(sys.argv)>3:
        contrast_factor = float(sys.argv[3])
    else:
        contrast_factor=None
    if len(sys.argv)>4:
        alpha = float(sys.argv[4])
    else:
        alpha=0.3
    if os.path.isfile(xml_dir):
        dfs = [convert.xml2df(xml_dir)]
    else:
        dfs = [convert.xml2df(os.path.join(xml_dir,s_i)) for s_i in os.listdir(xml_dir)]

    display_surveys(img,dfs,contrast_factor=contrast_factor,alpha=alpha)
