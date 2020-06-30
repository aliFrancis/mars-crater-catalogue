# Mars Crater Catalogue

## Overview

Repository holding a dataset for manually labelled small craters on Mars. Twelve images taken from CTX scenes over the MC11-East Quadrangle on Mars, each marked by six annotators. Agglomerative clustering is used to combine annotations.

## Usage examples

All commands below generally assume you are in the root directory of the project.

#### Cluster raw annotations and save output

> python ./src/cluster_surveys.py ./data/annotations/raw \<path/to/output\>  --\<options (see --help for details)\>


#### Agglomerative clustering visualisation

> python  ./src/cluster_slider.py  ./data/images/MC11E-A.png  ./data/annotations/raw/MC11E-A

#### Compute number of annotations and mean IoU for image
[can take a while for images with many annotations]

> python ./src/analysis.py ./data/annotations/raw/MC11E-B

#### Plot Crater Size-Frequency Distribution for all tiles

> python ./src/CSFDs.py

#### Compute diameter stats for all tiles

> python ./src/median_diameter.py

## Credits and Contributions

If you found this resource useful in your own work, please cite our upcoming paper, link tbc
