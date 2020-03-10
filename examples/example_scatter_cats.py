import plotille
#may need:  export PYTHONIOENCODING=utf8
import os
os.environ["PYTHONIOENCODING"]="utf8"

import numpy as np

import numpy

from numpy import cos, sin,min,max

#import pymap3d


def draw_scene(mouse_list, cat_list):
    
    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    fig.color_mode = 'names'


    listx = []
    listy = []
    names = []
    for mouse_index, mouse in enumerate(mouse_list):
        listx.append(mouse[0])
        listy.append(mouse[1])
        names.append("MOUSE %d" % (mouse_index))

    fig.scatter(listy,listx, lc='red', label='MOUSE',marker='o', text=names)   

    listx = []
    listy = []            
    for cat_index, cat in enumerate(cat_list):
        listx.append(cat[0])
        listy.append(cat[1])

    fig.scatter(listy,listx, lc='green', label='Cat', marker='x', text='Cat')# % (cat_index))        

    print(fig.show(legend=True))


    
if __name__ == "__main__":


    draw_scene([[-36, 108], [-36, 108.2], [-35.1, 108]],  [[-35.4, 108]])
    
