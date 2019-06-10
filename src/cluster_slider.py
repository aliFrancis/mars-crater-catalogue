import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.collections import EllipseCollection
import matplotlib.cm
import matplotlib.artist
import cluster_surveys
from data import convert
import distance


def get_update_func(nodelist,surveys):
    cmp = matplotlib.cm.ScalarMappable(norm=None, cmap='cool').get_cmap()
    def update(val):
        dist = sdist.val
        clusters = cluster_surveys.clusters_at_distance(nodelist,dist)
        colour_intensity = np.array([len(cluster) for cluster in clusters])
        cols = cmp(colour_intensity/N_surveyors)
        cols[:,-1] = 0.05+colour_intensity/15
        centres = convert.clusters2np(clusters,surveys)
        cluster_ec = EllipseCollection(widths=centres[:,2],heights=centres[:,2],angles=0,units='xy',
                                offsets = list(zip(centres[:,1],centres[:,0])),
                                transOffset=ax_main.transData,facecolors=cols,edgecolors = cols, linewidth=1)
        del ax_main.collections[0]
        ax_main.add_collection(cluster_ec)
        ax_hist.clear()
        n,bins,patches = ax_hist.hist([len(cluster) for cluster in clusters],[0.5+i for i in range(N_surveyors+1)],rwidth=0.4)
        for i,patch in enumerate(patches):
            patch.set_facecolor(color=cmp(i/N_surveyors))
        print(len(clusters),'    ',end='\r')
        ax_hist.grid(True)
        fig.canvas.draw_idle()

    return update

def reset(event):
    sdist.reset()

def toggle_vis(event):
    ax_main.collections[0].set_visible(not ax_main.collections[0].get_visible())
    fig.canvas.draw_idle()

if __name__=='__main__':
    import sys
    import os
    from skimage.io import imread

    img_path = sys.argv[1]
    img = imread(img_path)
    xml_dir = sys.argv[2]
    surveys = [convert.xml2df(os.path.join(xml_dir,s_i)) for s_i in os.listdir(xml_dir)]
    N_surveyors = len(surveys)
    nodelist = cluster_surveys.agglomerative(surveys,distance.negative_jaccard)
    fig= plt.figure()
    ax_main = plt.axes([0.2,0.12,0.75,0.75])
    dist = 0.5
    ax_main.imshow(img,cmap='gray')
    cmp = matplotlib.cm.ScalarMappable(norm=None, cmap='cool').get_cmap()
    clusters = cluster_surveys.clusters_at_distance(nodelist,dist)
    centres = convert.clusters2np(clusters,surveys)
    colour_intensity = np.array([len(cluster) for cluster in clusters])
    cols = cmp(colour_intensity/N_surveyors)
    cols[:,-1] = 0.05+colour_intensity/15

    cluster_ec = EllipseCollection(widths=centres[:,2],heights=centres[:,2],angles=0,units='xy',
                            offsets = list(zip(centres[:,1],centres[:,0])),
                            transOffset=ax_main.transData,facecolors=cols,edgecolors = cols, linewidth=1)
    ax_main.add_collection(cluster_ec)
    axcolor = 'lightgoldenrodyellow'

    ax_hist = plt.axes([0.05,0.05,0.18,0.6])
    n,bins,patches = ax_hist.hist([len(cluster) for cluster in clusters],[0.5+i for i in range(N_surveyors+1)],rwidth=0.4)
    for i,patch in enumerate(patches):
        patch.set_facecolor(color=cmp(i/N_surveyors))
    ax_hist.grid(True)

    ax_dist = plt.axes([0.35, 0.05, 0.5, 0.02], facecolor=axcolor)
    sdist = Slider(ax_dist, 'Max Dist', 0, 1, valinit=dist)

    sdist.on_changed(get_update_func(nodelist,surveys))

    reset_ax = plt.axes([0.05, 0.8, 0.1, 0.05])
    reset_button = Button(reset_ax, 'Reset', color=axcolor, hovercolor='0.975')
    reset_button.on_clicked(reset)

    vis_ax = plt.axes([0.05, 0.7, 0.1, 0.05])
    vis_button = Button(vis_ax, 'Set visibility', color=axcolor, hovercolor='0.975')
    vis_button.on_clicked(toggle_vis)


    plt.show()
