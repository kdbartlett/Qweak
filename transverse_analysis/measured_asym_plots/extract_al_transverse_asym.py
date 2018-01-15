#!/usr/bin/env python3

import numpy as np
import matplotlib as mpl
mpl.use('pgf')


def figsize(scale):
    fig_width_pt = 433.62001
    inches_per_pt = 1.0/72.0
    golden_mean = (np.sqrt(5.0)-1.0)/2.0
    fig_width = fig_width_pt*inches_per_pt*scale
    fig_height = fig_width*golden_mean
    fig_size = [fig_width, fig_height]
    return fig_size


